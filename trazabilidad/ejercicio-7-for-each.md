# Trazabilidad: módulo con `for_each`

- Se reemplazaron las dos llamadas al módulo local por un mapa `local.fichas` con las claves `portal` y `ayuda`.
- Un único bloque `module "fichas"` recorre el mapa con `for_each`; se esperan dos instancias: `module.fichas["portal"]` y `module.fichas["ayuda"]`.
- Cada instancia conserva su nombre y entorno: `portal-demo` y el entorno de la variable raíz para el portal; `portal-ayuda` y el mismo entorno para ayuda.
- La salida `resumen` recorre `module.fichas` con una expresión `for`, conserva las claves y toma el resumen de cada instancia.
- Se recuperó la política propia del ejercicio 6 para esta rama y se ajustaron únicamente las direcciones permitidas y las claves de portal/ayuda al mapa `module.fichas`.
- No se modificó `modulo_ficha/main.tf`.

No se ejecutó OpenTofu ni se hizo commit o Push.
