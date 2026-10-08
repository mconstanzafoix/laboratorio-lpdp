# Ejecución — regularización del Decreto supremo N° 662

## Apertura

- **REGLA:** `Fragmentador-de-Fuentes/PROMPT.md`, secciones 1–4: texto literal desde el PDF primario, unidad localizable, YAML cerrado, clasificación respaldada por marcador expreso, cotejo y reconstrucción por artículo.
- **HECHOS:** El primario, página 2, dice «Apruébase el reglamento…» y luego inicia «Artículo 1.- Objeto y ámbito de aplicación»; las páginas 2–10 contienen artículos 1–20. El PDF declara «Publicación: 09-SEP-2026 | Promulgación: 13-JUN-2025» y «Versión: Única De : 09-SEP-2026».
- **CUESTIÓN:** determinar la fidelidad, estructura, función y fuerza de cada unidad de esta Fuente y regularizar sus tarjetas sin alterar los literales ni la división de archivos.

## Estado y método

- 2026-09-30 22:47 -03: Leídos `AGENTS.md`, `Fragmentador-de-Fuentes/PROMPT.md`, `Fuentes-primarias/INDICE.md` e `INDICE.md`. `Fragmentador-de-Fuentes/MEMORY.md` no existe. El Orquestador confirmó que no hay compuerta ni perfil externo acreditado y que el encargo está autorizado.
- Captura previa estable comunicada por el Orquestador: `/tmp/lpdp-fragmentacion-previa-2026-09-30.tar.gz`. Línea base independiente: `/tmp/lpdp-regularizacion-baseline-2026-09-30.json`.
- Primario exacto: `Fuentes-primarias/Decreto-662-2026/Decreto-662_09-SEP-2026.pdf`, 10 páginas; SHA-256 calculado: `a7d436335f8b563733022f0beb6d395445b1fea8addfb2cb53057dce35896f7e`.
- Leídas las 10 páginas mediante `pypdf`; 127 literales de unidades menores localizados en la extracción primaria en orden, tras normalizar solo espacios/saltos de maquetación y quitar encabezados de página en los seis cruces. Se preservarán los bytes de esos bloques en la reescritura.
- Pendiente: regularizar unidades, luego `articulo.md` de cada carpeta, después `ARBOL.md`, `FUENTE.md` e `INFORME-FRAGMENTACION.md`; releer y comprobar.

## Decisiones de agente y pendientes

- Los sintagmas nominales enumerados del art. 3 dependen de «deberán contener» en el enunciado; la fuerza deóntica del literal propio no se completará con un verbo ausente. Se señalará la discrepancia cuando corresponda.
- Se revisarán las unidades indivisibles con marcadores de fuerza diferentes sin alterar la división autorizada. Su clasificación quedará parcial si el campo cerrado no puede reflejarla fielmente.
- La remisión «inciso siguiente» del art. 15, inc. 3, se conservará literal; se reportará su destino dudoso sin enmendarlo.

## Checkpoint de cierre — 2026-09-30 22:59:38 -03

- **Resultado:** parcial por clasificación cerrada de cuatro unidades indivisibles; cobertura textual de acto aprobatorio y artículos 1–20 comprobada. No se movió la Fuente a estado final jurídico.
- **Escrituras autorizadas:** 128 tarjetas con literal (127 unidades menores y acto aprobatorio), 20 fichas estructurales `articulo.md`, `ARBOL.md`, `FUENTE.md`, `INFORME-FRAGMENTACION.md` y este registro. No se modificaron otras Fuentes, PDF primarios ni resultados posteriores. Se conservaron nombres y división de archivos.
- **Orden:** en cada carpeta se escribieron primero unidades menores y al final `articulo.md`; luego el árbol, la ficha y el informe. El acto aprobatorio se trató como unidad equivalente sin número.
- **Método y relectura:** relectura de los 128 bloques literales desde su destino. Los 128 SHA-256 de bloque coinciden con la línea base previa; ninguno cambió byte a byte. En los 127 archivos de unidad se verificaron siete claves YAML exactas y los cinco títulos de cuerpo. Se comprobó que los 20 `articulo.md` no duplican literal, que 151 rutas de la Fuente coinciden con la línea base y que los enlaces internos del árbol y fichas resuelven. La reconstrucción ordenada de cada artículo coincide con el comienzo de su cuerpo extraído del PDF: 20 de 20. Se usó la página del PDF primario como localizador en cada tarjeta; seis bloques cruzan página.
- **Decisiones de agente:** se clasificó la facultad de la Agencia en art. 3, letra g, párrafo 2, fragmento 2, como `Constitutiva` porque «podrá… establecer» atribuye competencia y «debe entenderse» delimita ese ejercicio. Los sintagmas nominales del art. 3 reciben `Sin marcador expreso` deóntico cuando la fórmula «deberán contener» está solo en el enunciado enlazado. No son decisiones humanas ni visados.
- **Parciales:** art. 6, inc. 1, frag. 1 (permiso y obligación); art. 15, inc. 4 (vigencia constitutiva y permiso de renovación); art. 18, inc. 1 (realización y permiso anticipado); art. 19, inc. 2, frag. 3 (permiso de reserva y deber de justificar). Se mantuvieron literales y cortes; campos deónticos —y en art. 15 inc. 4 también tipo— vacíos y `[parcial]` en el árbol, con explicación localizada en cada tarjeta y el informe.
- **Hallazgo remitido:** art. 15, inc. 3, página 8, «inciso siguiente» apunta textualmente al inciso cuarto, que trata vigencia y renovación; el registro se desarrolla en art. 17. Destino dudoso, sin corrección conjetural ni afirmación de error confirmado. No se creó Escalada.
- **Dependencias y decisión humana:** la Fuente podrá alimentar comprobaciones posteriores solo con advertencia de sus cuatro parciales y de la remisión dudosa. No se registró decisión humana; el Orquestador debe encaminar el hallazgo y mantener la clasificación parcial hasta resolver la incompatibilidad del campo cerrado con los cortes preservados.
- **Reanudación:** partir de `INFORME-FRAGMENTACION.md` y `ARBOL.md`; cotejar cualquier cambio futuro con el PDF de SHA-256 indicado en `FUENTE.md` y la captura anterior `/tmp/lpdp-fragmentacion-previa-2026-09-30.tar.gz`. No repetir cortes ni resolver la remisión por inferencia.
