# Trazabilidad: catálogo de fichas (ejercicio 7)

## Estado actual

- Rama de trabajo: `catalogo-ejercicio-7`.
- `main.tf` define `local.catalogo` con las claves `portal` y `ayuda`. `module "fichas"` recorre el mapa con `for_each`; ambas instancias reciben `var.entorno`.
- `outputs.tf` construye `resumen` con una expresión `for`, manteniendo las claves del catálogo.
- `politica_plan.py` permite exactamente las direcciones de `portal` y `ayuda` y conserva las comprobaciones del ejercicio 6. Se verificó con JSON sintético: el caso permitido pasa y direcciones antiguas o entornos distintos se rechazan.
- El workflow `.github/workflows/validacion.yml` no fue modificado y no ejecuta `politica_plan.py`. Por ello, las pruebas con tres cambios en Actions pasaron sus planes; no fueron rechazos de política en CI. La política sí rechazaría tres cambios si se ejecutase.
- No se modificó `modulo_ficha/main.tf` ni se ejecutó `tofu apply`. No hubo despliegue. El stash `respaldo-antes-ejercicio-6` permanece intacto.

## Commits y ejecuciones de Actions

| Commit | Cambio | Ejecución y resultado |
| --- | --- | --- |
| `9de126b` | Catálogo inicial con `for_each`, salida `resumen` y adaptación de direcciones de la política. | [Run 34](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44708913457): éxito. |
| `a4862e7` | Prueba temporal de tercera ficha con la representación inicial del mapa. | [Run 35](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44709919962): éxito; el plan mostró 3 altas. El workflow no ejecutó la política. |
| `5b24a28` | Retirada de esa ficha temporal. | [Run 36](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44710108325): éxito. |
| `fb6fd3f` | Repetición de la prueba con el mapa plano `catalogo` y `informes`. | [Run 37](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44710966800): éxito; ambos planes mostraron `3 to add`, incluido `module.fichas["informes"].terraform_data.ficha`. El workflow no ejecutó la política. |
| `633585a` | Retirada de `informes` y conservación de las claves `portal` y `ayuda`. | [Run 38](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44711081518): fallo en `tofu fmt -check -diff -recursive` por alineación. |
| `be0a3d4` | Corrección de alineación indicada por OpenTofu fmt. | [Run 39](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44711767123): éxito. |
| `6a65f21` | Sección `## Catálogo de fichas` en el README. | [Run 40](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44712243438): éxito. |
