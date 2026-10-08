# Documentos canónicos del Sistema LPDP — README

Reconstrucción consolidada del sistema 🧪 Laboratorio LPDP, generada el 25-09-2026. Fechas en DD-MM-AAAA; los archivos se citan por su nombre real. 🆕 *(30-09-2026: este paquete se trasladó a `Laboratorio LPDP/Insumos/planificacion/documentos-canonicos/` — traspaso real, no copia: **esta es la única ubicación vigente del canon** — con renombrado de `INDICE.md`→`README.md` y `00-Sistema-LPDP-Consolidado.md`→`00-Sistema-LPDP.md`)*

## Documentos canónicos (lo permanente)

| Archivo | Qué contiene | Para quién |
|---|---|---|
| `00-Sistema-LPDP.md` | El sistema explicado de inicio a fin: propósito, piezas, cada ciclo etapa por etapa con su agente, su entrega y su tabla de propiedades | lectura completa, humana e IA |
| `01-Bases-de-Datos-y-Propiedades.md` | Las 10 bases de Notion con todas sus propiedades, valores, la regla de equivalencia del Identificador y restricciones técnicas | referencia de esquema |
| `02-Gobernanza-y-Context-Engineering.md` | Fuentes únicas de verdad, contratos de traspaso, AGENTS.md consolidado, uso de SKILL.md/MEMORY.md, retención, proveniencia (con explicación de SHA-256), divulgación progresiva y catálogo de anti-patrones | gobierno del sistema |

*(El antiguo `01-Contratos-de-Agentes.md` se retiró del paquete el 30-09-2026 — minuta 8: su contenido vive en el `AGENTS.md` y los `PROMPT.md` de la carpeta de agentes; antecedente histórico en `/Users/mcfoix/Desktop/Gestion del Caos/antecedentes-historicos-superados/`.)*

## La carpeta de agentes (convención, minuta 10)

El canon nombra a la carpeta de agentes **por función** («la carpeta de agentes», «el `PROMPT.md` del Fragmentador», «el `AGENTS.md`») y **no** por su nombre de carpeta, que es circunstancial. Si cambia, se actualiza esta línea y ningún documento canónico se rompe.

**Nombre y ubicación vigentes (02-10-2026):**

| Instancia | Ubicación | Rol |
|---|---|---|
| `harness-md-lpdp/` | `/Users/mcfoix/Desktop/Laboratorio LPDP/Insumos/planificacion/harness-md-lpdp/` | **Fuente vigente y única de las instrucciones despachables**: `AGENTS.md`, un `PROMPT.md` por agente y las skills obligatorias declaradas por el Destilador en `skills/examen-intensivo-destilacion/SKILL.md` y `skills/calificar-sancion-exigencia/SKILL.md`; `MEMORY.md` solo si existe y aporta algo no recuperable desde los productos y `Ejecuciones/` |
| `workspace-lpdp/` | `/Users/mcfoix/Desktop/Gestion del Caos/6. Consolidado/workspace-lpdp/` | Antecedente histórico; no es fuente de despacho ni se sincroniza bidireccionalmente con el harness |

## Operación y decisiones (fuera de los documentos canónicos)

| Archivo | Qué contiene | Para quién |
|---|---|---|
| `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/Propuestas-pendientes.md` | Propuestas de diseño en ⏳ standby con su contexto completo (contenedor `disposiciones/` en la carpeta de Fuente; P-02 huella SHA-256 al cotejar literales; P-03 desglose de campos YAML compuestos) | decisiones diferidas de MCF |
| `/Users/mcfoix/Desktop/Gestion del Caos/informes/04-Diagnosticos-y-Desfases.md` | 13 desfases detectados con corrección propuesta y matriz de prioridad — registro operativo, no canon | operación |
| `/Users/mcfoix/Desktop/Gestion del Caos/informes/05-Reglas-de-Testeo-y-Corridas.md` | Compuertas C0–C6, excepciones E-01/E-02, perfiles `i0.x` y estado de la campaña de testeo. **Nada ahí es canónico** | operación |
| `/Users/mcfoix/Desktop/Gestion del Caos/Minutas de decision/` | Minutas de decisión visadas por MCF (28, 29 y 30-09-2026), incluido el traspaso en limpio de los Estados de los documentos canónicos al 30-09-2026 | registro de decisiones |

**Estado:** se conservan los visados anteriores donde constan; los ajustes solicitados el 01-10-2026 y el 02-10-2026 en contratos y documentos canónicos están incorporados para revisión y no se presentan como visados posteriores. Los documentos 00–02 son la referencia canónica del diseño; su promoción se rige por `02-Gobernanza-y-Context-Engineering.md` §10.
**Regla de este paquete:** si este índice se desactualiza, es un defecto reportable (ver `02-Gobernanza-y-Context-Engineering.md`, §3).

## Árbol del paquete y orden de lectura

Mapa completo antes del detalle: un agente (o persona) que aterrice aquí ve el esqueleto del sistema sin navegar. Anotaciones: **[canon]** permanente · **[referencia]** esquema/gobierno.

```
documentos-canonicos/
├── README.md                              ← este archivo: mapa + regla de índice sano
├── 00-Sistema-LPDP.md                     [canon] el sistema de inicio a fin (ciclos, etapas, agentes, tablas)
├── 01-Bases-de-Datos-y-Propiedades.md     [referencia] esquema de las 10 bases de Notion + equivalencias
└── 02-Gobernanza-y-Context-Engineering.md [referencia] SSOT, traspasos, retención, anti-patrones
```

**Orden de lectura según tu rol:**

| Si eres… | Lee en este orden | No cargues |
|---|---|---|
| Humano que quiere entender el sistema | 00 → este README → 01/02 según duda | `informes/` (salvo que operes corridas) |
| Agente con encargo operativo | `AGENTS.md` del harness → tu `<Rol>/PROMPT.md` → skill obligatoria declarada allí, si la hay → `MEMORY.md` solo si existe → perfil aplicable, si existe → encargo | 00–02 completos (salvo remisión expresa); casos de control de la skill que no correspondan a la duda |
| Agente de Arquitectura | 01 → 02 → este README | — |
| Quien audita gobernanza | 02 → `04-Diagnosticos-y-Desfases.md` → verificación de índices | — |

**Verificación del índice:** 4 entradas listadas (4 archivos de este paquete) — última comprobación 02-10-2026 contra disco. Quien agregue o renombre un archivo sin actualizar este árbol deja un defecto reportable.
