import json
import sys


EXPECTED_ADDRESSES = {
    "module.fichas[\"portal\"].terraform_data.ficha",
    "module.fichas[\"ayuda\"].terraform_data.ficha",
}
EXPECTED_PROJECT = "nexo-portal"
EXPECTED_TEAMS = {
    "desarrollo": "equipo-desarrollo",
    "pruebas": "equipo-pruebas",
    "integracion": "equipo-integracion",
}
ALLOWED_ENVIRONMENTS = set(EXPECTED_TEAMS)


def reject(reason):
    print(f"POLÍTICA RECHAZADA: {reason}")
    return 1


def is_marked(flags, field):
    if flags is True:
        return True
    if not isinstance(flags, dict):
        return False

    input_flags = flags.get("input")
    if input_flags is True:
        return True
    return isinstance(input_flags, dict) and input_flags.get(field) is True


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

        after_unknown = change.get("after_unknown")
        after_sensitive = change.get("after_sensitive")
        values = {}
        for field in ("nombre", "proyecto", "entorno", "equipo"):
            if is_marked(after_unknown, field):
                return reject(f"{address}: {field} está marcado como desconocido")
            if is_marked(after_sensitive, field):
                return reject(f"{address}: {field} está marcado como sensible")
            value = input_values.get(field)
            if not isinstance(value, str) or not value:
                return reject(f"{address}: {field} falta o no es un texto conocido")
            values[field] = value
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
        if values["proyecto"] != EXPECTED_PROJECT:
            return reject(
                f"proyecto incorrecto para {label}: se esperaba "
                f"{EXPECTED_PROJECT!r}, se recibió {values['proyecto']!r}"
            )
        expected_team = EXPECTED_TEAMS[values["entorno"]]
        if values["equipo"] != expected_team:
            return reject(
                f"equipo incorrecto para {label} en {values['entorno']!r}: "
                f"se esperaba {expected_team!r}, se recibió {values['equipo']!r}"
            )
    if portal["entorno"] != help_ficha["entorno"]:
        return reject(
            "los entornos no coinciden: "
            f"portal={portal['entorno']!r}, ayuda={help_ficha['entorno']!r}"
        )

    print(
        "POLÍTICA APROBADA: dos fichas con proyecto, entorno y equipo válidos"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
