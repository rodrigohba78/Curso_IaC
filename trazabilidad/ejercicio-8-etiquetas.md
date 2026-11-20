# Trazabilidad: etiquetas didácticas (ejercicio 8)

## Cambio final

- Se conservan las dos fichas, el módulo local, los escenarios predeterminado e integración y el workflow existente.
- Cada `terraform_data.ficha` recibe `proyecto`, `entorno` y `equipo`, además de `nombre`. El proyecto común es `nexo-portal`.
- El escenario predeterminado usa `equipo-pruebas`; `escenario-integracion.tfvars` usa `equipo-integracion`.
- La política valida que las cuatro entradas sean conocidas y no sensibles, que el proyecto sea el esperado y que el equipo corresponda al entorno. Se mantienen las dos direcciones permitidas y las comprobaciones anteriores.
- Decisión de diseño: `equipo_responsable` es una entrada de escenario sin validación cruzada en OpenTofu. Así, una asignación equivocada puede llegar al plan y la política demuestra que puede detectarla aunque `validate` y `plan` pasen.
- El workflow no se modificó: ya guarda y evalúa ambos planes con `politica_plan.py`. No se ejecutó `tofu apply`; las etiquetas son datos ficticios de `terraform_data`.

## Commits y ejecuciones

| Commit | Cambio | Ejecución y resultado |
| --- | --- | --- |
| `0c83137` | Añadidas las etiquetas y las reglas de propiedad. | [Run 45](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44727614059): falló en formato por la alineación de `escenario-integracion.tfvars`; todavía no llegó a validar ni planificar. |
| `e9b7d3c` | Corregida la alineación indicada por OpenTofu fmt. | [Run 46](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44727907088): verde; formato, validación, los dos planes y las dos políticas pasaron. |
| `bef1fc2` | Prueba controlada: integración asignada temporalmente a `equipo-pruebas`. | [Run 47](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44728127663): planes verdes; `Politica del plan de integracion` rechazó el equipo incorrecto. El resumen y el artefacto se publicaron y el trabajo terminó rojo. |
| `97530d5` | Restaurado `equipo-integracion`. | [Run 48](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44728262707): verde; ambas políticas pasaron. |

La política también se probó localmente con JSON sintético: aprobó pruebas/equipo-pruebas e integración/equipo-integracion, y rechazó integración/equipo-pruebas. El stash `respaldo-antes-ejercicio-6` se mantuvo intacto.
