# Trazabilidad: etiquetas didácticas (ejercicio 8)

## Historial de la implementación anterior

Los siguientes commits y ejecuciones documentan la primera versión del ejercicio, que usaba campos planos `proyecto` y `equipo`. Se conservan como historial; esa estructura se está alineando ahora con el esquema anidado de la guía.

| Commit | Cambio | Ejecución y resultado |
| --- | --- | --- |
| `0c83137` | Añadidas las etiquetas y las reglas de propiedad. | [Run 45](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44727614059): falló en formato por la alineación de `escenario-integracion.tfvars`; todavía no llegó a validar ni planificar. |
| `e9b7d3c` | Corregida la alineación indicada por OpenTofu fmt. | [Run 46](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44727907088): verde con la estructura plana anterior. |
| `bef1fc2` | Prueba controlada: integración asignada temporalmente a `equipo-pruebas`. | [Run 47](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44728127663): planes verdes; la política de integración rechazó el equipo incorrecto y el trabajo terminó rojo. |
| `97530d5` | Restaurado `equipo-integracion`. | [Run 48](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44728262707): verde con la estructura plana anterior. |

## Corrección local conforme a la guía

En la rama `taller-final-ejercicio-8`, sobre el punto de partida `290fbf2`, se alinearon los seis archivos técnicos con la guía y se publicaron en `c640297` y `b4be799`. El README y esta trazabilidad se publicaron en `cd87fc3`.

- La variable raíz se llama `responsable` y su valor predeterminado es `equipo-lab`. El valor aprobado para integración es `equipo-integracion`; en la prueba de la sección 9 se cambia temporalmente a `equipo-lab`.
- La raíz pasa `responsable` al módulo. El módulo declara esa entrada y estructura `terraform_data.input` con `nombre`, `entorno` y el mapa `etiquetas` (`proyecto`, `entorno`, `responsable`).
- La política conserva las dos direcciones y las reglas del ejercicio. Comprueba las claves exactas de `input` y `etiquetas`, recorre recursivamente las marcas `unknown` y `sensitive`, y asigna `equipo-lab` a desarrollo/pruebas y `equipo-integracion` a integración.
- El rechazo de una asignación incorrecta en integración es `POLÍTICA RECHAZADA: responsable no aprobado para integracion`.
- Se actualizó el README para describir la estructura anidada. No se modificaron el workflow ni las salidas de la raíz.

### Sección 4 — Pasar el dato al módulo

- En el bloque `module "fichas"` de la raíz, `responsable = var.responsable` alimenta cada instancia.
- `local.catalogo` conserva únicamente las claves `portal` y `ayuda`.
- `modulo_ficha/variables.tf` declara `responsable` como `string`, por lo que coincide el argumento que envía la raíz con la entrada que acepta el módulo.
- La revisión del diff y `git diff --check` pasaron. No se ejecutó `tofu validate` ni Actions; esta comprobación de ejecución queda pendiente de publicar los cambios.

### Sección 5 — Describir las etiquetas ficticias

- Comparé `modulo_ficha/main.tf` con el bloque indicado en la guía: `terraform_data.ficha.input` contiene `nombre`, `entorno` y `etiquetas`, con `proyecto = "nexo-portal"`, el entorno de la variable y el responsable de la variable.
- El bloque coincide con la alineación deliberada del ejemplo; no fue necesario modificar el código en esta sección.
- `modulo_ficha/outputs.tf` ya expone `terraform_data.ficha.input`, así que las etiquetas forman parte de `resumen` sin cambiar las salidas.
- `git diff --check` pasó. No se ejecutó `tofu fmt`, `tofu validate`, `tofu plan` ni Actions; esas comprobaciones siguen pendientes.

### Sección 6 — Ampliar la política sin perder controles

- La política define el responsable esperado para cada entorno y consulta ese mapa solo después de comprobar que el entorno está permitido.
- `contains_true` recorre mapas y listas, por lo que las marcas anidadas con `False` no se confunden con valores desconocidos y cualquier `True` se rechaza.
- Se comprueban exactamente las claves `nombre`, `entorno`, `etiquetas` y, dentro de `etiquetas`, `proyecto`, `entorno`, `responsable`.
- Se conservan las dos direcciones de `module.fichas`, el tipo `terraform_data`, la acción `create`, los nombres `portal-*`, la ayuda fija `portal-ayuda`, el proyecto `nexo-portal` y la igualdad de entornos.
- La salida de aprobación coincide con el texto requerido por la guía. Las pruebas sintéticas aprobaron los escenarios válidos y rechazaron equipo incorrecto, marcas `unknown`/`sensitive`, claves extra, dirección antigua, tercera ficha, entorno no permitido y acción distinta de `create`.
- `git diff --check` pasó. No se ejecutaron OpenTofu ni Actions; el resultado de integración aún debe comprobarse en el workflow.

### Sección 7 — Revisión crítica del recorrido

- Recorrido revisado: `variables.tf` → argumento `responsable` en el módulo de la raíz → variable `responsable` del módulo → `terraform_data.ficha.input.etiquetas` → valores del plan → comprobación de `politica_plan.py`.
- Afirmación: `tofu validate` puede aprobar aunque integración reciba `equipo-lab`, porque sigue siendo un `string` válido. La política aplica la regla de negocio y debe rechazarlo; el paso 9 propone comprobarlo con una ejecución controlada.
- Comprobaciones propuestas en Actions: `Validar` termina correctamente; cada paso de plan muestra dos altas y los valores ficticios esperados; ambas políticas escriben `POLÍTICA APROBADA` en la ejecución verde. En la prueba controlada posterior, integración debe mostrar el rechazo esperado.
- Límite: la política vive en la misma rama y puede modificarse junto con la configuración; `terraform_data` solo simula metadatos y no demuestra etiquetado cloud, gobierno independiente ni despliegue.
- Es una revisión conceptual; no se modificó código ni se ejecutó Actions en esta sección.

### Sección 8 — Primera publicación y corrección de formato

- Commit `c640297` (`Ejercicio 8: etiquetas y responsables gobernados`) publicó los seis archivos técnicos en `taller-final-ejercicio-8`.
- [Run 50](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44733021301) inicializó OpenTofu, pero falló en `Comprobar formato`: `escenario-integracion.tfvars` necesitaba una columna menos de espacios antes de `=`. Validación, planes y políticas quedaron omitidos; el resumen y el artefacto se generaron.
- Se corrigió la alineación de las tres asignaciones en `escenario-integracion.tfvars`; Run 50 no verifica validación ni planes.
- El commit `b4be799` publicó la corrección. [Run 51](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44733201549) pasó formato, validación, los dos planes y las dos políticas. Ambos planes mostraron `Plan: 2 to add, 0 to change, 0 to destroy`; pruebas mostró `nexo-portal`/`equipo-lab`, integración `nexo-portal`/`equipo-integracion`, y las dos políticas aprobaron.
- El resumen registró las seis comprobaciones en verde y se publicó `evidencia.txt` como artefacto con retención de siete días. No se ejecutó `tofu apply`.

### Sección 9 — Rechazo controlado en integración

- Antes de publicar, la predicción fue: el escenario predeterminado y su política siguen verdes; el plan de integración también pasa con `responsable = "equipo-lab"`, pero su política rechaza esa asignación.
- Solo se cambió la última línea de `escenario-integracion.tfvars`. El commit `26f0849` (`Prueba: responsable de integracion incorrecto`) publicó el valor temporal en la rama.
- [Run 52](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44733699455) confirmó la predicción: formato, validación, plan y política predeterminados y plan de integración pasaron; la política de integración terminó con `POLÍTICA RECHAZADA: responsable no aprobado para integracion`.
- El trabajo quedó rojo intencionalmente. El resumen mostró la política de integración como `failure` y `evidencia.txt` se publicó; no se ejecutó `tofu apply`.
- La rama queda en este estado de prueba. En la sección 10 habrá que restaurar `equipo-integracion` y obtener una ejecución verde.

### Sección 10.1 — Restaurar el responsable aprobado

- El commit `5ccd24c` (`Correccion: responsable aprobado en integracion`) restauró únicamente `responsable = "equipo-integracion"` y se publicó en la misma rama.
- [Run 53](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44734089396) quedó verde: formato, validación, los dos planes y las dos políticas pasaron. Cada plan mostró dos altas; el predeterminado usó `equipo-lab` y el de integración `equipo-integracion`.
- No se ejecutó `tofu apply`.
- El responsable de integración ya está restaurado.

### Sección 10.2 — Documentar el taller

- El README describe las dos claves del catálogo, las etiquetas ficticias, la regla de responsable por entorno, el rechazo controlado de `equipo-lab` en integración y que el laboratorio no despliega infraestructura.
- El commit `cd87fc3` publicó el README y esta trazabilidad. [Run 54](https://github.com/rodrigohba78/Curso_IaC/actions/runs/44734355685) comprobó ese commit y quedó verde en formato, validación, los dos planes y las dos políticas.
- El README también deja claro que no se ejecuta `apply`.

## Comprobaciones locales de esta corrección

- `git diff --check`: correcto.
- Política con JSON sintético: aprobaron pruebas/`equipo-lab` e integración/`equipo-integracion`.
- La política rechazó integración/`equipo-lab` con el mensaje esperado.
- Las marcas anidadas `unknown` y `sensitive` en `true`, y una clave adicional en `etiquetas`, fueron rechazadas. Las marcas anidadas en `false` no produjeron un falso positivo en los dos casos aprobados.
- OpenTofu ejecutó formato, validación y planes únicamente en Actions (Run 51); `tofu apply` no se ejecutó.
