import json
import sys


EXPECTED_ADDRESSES = {
    "module.fichas[\"portal\"].terraform_data.ficha",
    "module.fichas[\"ayuda\"].terraform_data.ficha",
}
EXPECTED_PROJECT = "nexo-portal"
RESPONSIBLE_BY_ENVIRONMENT = {
    "desarrollo": "equipo-lab",
    "pruebas": "equipo-lab",
    "integracion": "equipo-integracion",
}
ALLOWED_ENVIRONMENTS = set(RESPONSIBLE_BY_ENVIRONMENT)
EXPECTED_INPUT_KEYS = {"nombre", "entorno", "etiquetas"}
EXPECTED_LABEL_KEYS = {"proyecto", "entorno", "responsable"}


def reject(reason):
    print(f"POLÍTICA RECHAZADA: {reason}")
    return 1


def contains_true(value):
    if value is True:
        return True
    if isinstance(value, dict):
        return any(contains_true(item) for item in value.values())
    if isinstance(value, list):
        return any(contains_true(item) for item in value)
    return False


def is_marked(flags, field):
    if flags is True:
        return True
    if not isinstance(flags, dict):
        return False
    input_flags = flags.get("input")
    if isinstance(input_flags, dict):
        return contains_true(input_flags.get(field))
    return contains_true(input_flags)


def main():
    try:
        plan = json.load(sys.stdin)
    except json.JSONDecodeError as error:
        return reject(
            f"JSON no válido en línea {error.lineno}, columna {error.colno}: {error.msg}"
        )
    except UnicodeDecodeError:
        return reject("la entrada no contiene texto UTF-8 válido")

    if not isinstance(plan, dict):
        return reject("el documento JSON debe ser un objeto")

    resource_changes = plan.get("resource_changes")
    if not isinstance(resource_changes, list):
        return reject("falta resource_changes o no es una lista")
    if len(resource_changes) != 2:
        return reject(
            f"se esperaban exactamente dos cambios; se recibieron {len(resource_changes)}"
        )

    changes_by_address = {}
    for item in resource_changes:
        if not isinstance(item, dict):
            return reject("cada elemento de resource_changes debe ser un objeto")
        address = item.get("address")
        if not isinstance(address, str):
            return reject("cada cambio debe tener una dirección de texto")
        if address not in EXPECTED_ADDRESSES:
            return reject(f"dirección inesperada: {address!r}")
        if address in changes_by_address:
            return reject(f"dirección repetida: {address}")
        changes_by_address[address] = item

    missing_addresses = EXPECTED_ADDRESSES - changes_by_address.keys()
    if missing_addresses:
        return reject(
            "faltan direcciones requeridas: " + ", ".join(sorted(missing_addresses))
        )

    values_by_address = {}
    for address in sorted(EXPECTED_ADDRESSES):
        item = changes_by_address[address]
        if item.get("mode") != "managed":
            return reject(f"{address}: el recurso debe ser managed")
        if item.get("type") != "terraform_data":
            return reject(f"{address}: el tipo debe ser terraform_data")

        change = item.get("change")
        if not isinstance(change, dict):
            return reject(f"{address}: falta el objeto change")
        if change.get("actions") != ["create"]:
            return reject(f"{address}: la única acción permitida es [\"create\"]")

        after = change.get("after")
        if not isinstance(after, dict):
            return reject(f"{address}: change.after debe ser un objeto")
        input_values = after.get("input")
        if not isinstance(input_values, dict):
            return reject(f"{address}: falta change.after.input")
        if set(input_values) != EXPECTED_INPUT_KEYS:
            return reject(
                f"{address}: change.after.input debe contener exactamente "
                "nombre, entorno y etiquetas"
            )
        labels = input_values.get("etiquetas")
        if not isinstance(labels, dict):
            return reject(f"{address}: etiquetas debe ser un mapa")
        if set(labels) != EXPECTED_LABEL_KEYS:
            return reject(
                f"{address}: etiquetas debe contener exactamente "
                "proyecto, entorno y responsable"
            )

        after_unknown = change.get("after_unknown")
        after_sensitive = change.get("after_sensitive")
        for field in ("nombre", "entorno", "etiquetas"):
            if is_marked(after_unknown, field):
                return reject(f"{address}: {field} está marcado como desconocido")
            if is_marked(after_sensitive, field):
                return reject(f"{address}: {field} está marcado como sensible")

        values = {}
        for field in ("nombre", "entorno"):
            value = input_values.get(field)
            if not isinstance(value, str) or not value:
                return reject(f"{address}: {field} falta o no es un texto conocido")
            values[field] = value
        label_values = {}
        for field in ("proyecto", "entorno", "responsable"):
            value = labels.get(field)
            if not isinstance(value, str) or not value:
                return reject(
                    f"{address}: etiquetas.{field} falta o no es un texto conocido"
                )
            label_values[field] = value
        values["etiquetas"] = label_values
        values_by_address[address] = values

    portal_address = "module.fichas[\"portal\"].terraform_data.ficha"
    help_address = "module.fichas[\"ayuda\"].terraform_data.ficha"
    portal = values_by_address[portal_address]
    help_ficha = values_by_address[help_address]

    if not portal["nombre"].startswith("portal-"):
        return reject("el nombre del portal debe comenzar por portal-")
    if not help_ficha["nombre"].startswith("portal-"):
        return reject("el nombre de la ayuda debe comenzar por portal-")
    if help_ficha["nombre"] != "portal-ayuda":
        return reject("el nombre de la ayuda debe ser exactamente portal-ayuda")

    for label, values in (("portal", portal), ("ayuda", help_ficha)):
        if values["entorno"] not in ALLOWED_ENVIRONMENTS:
            return reject(f"entorno no permitido para {label}: {values['entorno']!r}")
        labels = values["etiquetas"]
        if labels["proyecto"] != EXPECTED_PROJECT:
            return reject(
                f"proyecto incorrecto para {label}: se esperaba "
                f"{EXPECTED_PROJECT!r}, se recibió {labels['proyecto']!r}"
            )
        if labels["entorno"] != values["entorno"]:
            return reject(
                f"etiquetas.entorno no coincide para {label}: "
                f"{labels['entorno']!r} != {values['entorno']!r}"
            )
        expected_responsible = RESPONSIBLE_BY_ENVIRONMENT.get(values["entorno"])
        if expected_responsible is None:
            return reject(f"no hay responsable aprobado para {values['entorno']!r}")
        if labels["responsable"] != expected_responsible:
            return reject(f"responsable no aprobado para {values['entorno']}")
    if portal["entorno"] != help_ficha["entorno"]:
        return reject(
            "los entornos no coinciden: "
            f"portal={portal['entorno']!r}, ayuda={help_ficha['entorno']!r}"
        )

    print(
        "POLÍTICA APROBADA: dos fichas con etiquetas y responsable ficticios correctos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
