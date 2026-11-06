# MesaTCG · Matriz de trazabilidad (Sprint 1)

**Sprint Goal:** que dos jugadores puedan resolver tiradas y llevar el puntaje de su partida desde un celular.
**Sprint Backlog:** HU-01 (3 pts) + HU-02 (3 pts) = 6 pts.
**Cómo leer esta matriz:** cada fila une un criterio de aceptación con el código que lo implementa, la prueba que lo verifica y lo que se muestra en el video. Para regenerar la evidencia de pruebas, ejecuta `pytest`. La salida lista cada test con su HU y su CA.

Estados: **OK** verificado · **Pendiente** falta verificar · **Fuera** no entra en este sprint

---

## HU-01 · Lanzar dado (3 pts)

| CA / Requisito | Implementación | Prueba automatizada | Verificación en pantalla | Estado |
|---|---|---|---|---|
| **CA1** valor dentro del rango (d6/d20) · RF-01 | `app/dominio/dado.py` → `lanzar()` · `app/main.py` → `POST /api/dado` | `test_HU01_CA1_*` (5 tests) | Panel de dado: elegir d6/d20 y pulsar "Lanzar" | OK |
| **CA2** resultado en grande que reemplaza al anterior · RF-02 | API devuelve una sola tirada · `index.html` → `#resultado` (160 px) | `test_HU01_CA2_api_devuelve_un_solo_resultado_por_tirada` | Tirar varias veces: el número cambia, no se acumula | OK |
| **RNF-02** respuesta en < 1 s | FastAPI local, sin base de datos | `test_HU01_RNF02_tirada_responde_en_menos_de_1_segundo` | Respuesta instantánea al pulsar | OK local, Pendiente en Render |
| **RNF-04** equidad de caras | `secrets.randbelow()` (azar del sistema operativo) | `test_HU01_RNF04_distribucion_uniforme` (60 000 tiradas d6 y 100 000 d20) | No aplica | OK |

## HU-02 · Marcador de puntaje (3 pts)

| CA / Requisito | Implementación | Prueba automatizada | Verificación en pantalla | Estado |
|---|---|---|---|---|
| **CA1** dos nombres + meta, parten en 0 · RF-03 | `app/dominio/marcador.py` → `Partida.__init__` · `POST /api/partidas` | `test_HU02_CA1_*` (7 tests) | Pantalla de configuración → marcador en 0 a 0 | OK |
| **CA2** +1 / −1, nunca baja de 0 · RF-04 | `Partida.sumar()` / `Partida.restar()` con `max(0, …)` | `test_HU02_CA2_*` (6 tests) | Pulsar −1 con el marcador en 0: sigue en 0 | OK |
| **CA3** anuncia al ganador · RF-05 | propiedad `Partida.ganador` · aviso `#ganador` en `index.html` | `test_HU02_CA3_*` (3 tests) | Llegar a la meta → "¡Ganó …!" | OK |
| **RNF-01** uso con una mano, lectura a 1 m | botones de 64 px de alto, puntaje de 96 px, dado de 160 px | No aplica (es visual) | Probar en un celular real sobre la mesa | OK en navegador, Pendiente en celular real |

## RNF transversal

| Requisito | Implementación | Verificación | Estado |
|---|---|---|---|
| **RNF-03** funciona en el navegador del celular sin instalar nada | `GET /` sirve la página; fuentes autoalojadas en `/static/fonts/`, sin servicios externos | `tests/test_interfaz.py` (4 tests) + abrir la URL en el celular | OK vista móvil, Pendiente en celular real |

## Decisiones de diseño (para defender en el video)

1. **El marcador se congela al haber ganador.** La HU no lo dice explícitamente, pero sin esta regla un toque accidental cambiaría el resultado ya anunciado (CA3). Para jugar otra partida aparece "Nueva partida". Prueba: `test_HU02_CA3_con_ganador_el_marcador_queda_congelado`.
2. **Cada mesa tiene su propia partida (id).** Si dos mesas usan la misma URL, sus marcadores no se mezclan. Prueba: `test_HU02_partidas_de_distintas_mesas_no_se_mezclan`.
3. **"Nueva partida" solo aparece al terminar y no pide confirmación.** La confirmación antes de borrar es HU-03 CA3 (Sprint 2).
4. **Las reglas viven solo en Python** (`app/dominio/`). La interfaz no calcula nada, solo muestra lo que responde la API.
5. **Validación en dos capas.** La API rechaza datos mal formados (422) y el dominio vuelve a validar (por ejemplo, un nombre de solo espacios).
6. **−1 y +1 se distinguen por forma, no solo por color.** El −1 es un botón hueco y el +1 uno relleno. Así se distinguen con luz baja o con daltonismo (RNF-01).
7. **Un solo color de acento (brasa).** Se reserva para la acción principal, el resultado del dado, el jugador que va ganando y el anuncio del ganador. La vista dirige la mirada a lo importante.

## Fuera del Sprint 1

| Ítem | Motivo |
|---|---|
| HU-03 historial y conservación (RF-06, RF-07) | Sprint 2: entra MongoDB (colecciones `partidas` y `eventos`) |
| HU-04 contadores adicionales · HU-05 temporizador | Sin refinar ni estimar (backlog DEEP) |
| Cuentas de usuario, juego en línea | Descartado: fuera del Sprint Goal y del ámbito |
| Otros dados (d4, d8, d12…) | No están en HU-01; requieren refinar la historia |

## Definition of Done · checklist por historia

| Ítem DoD | HU-01 | HU-02 |
|---|---|---|
| 1. Cumple todos sus CA | OK | OK |
| 2. RNF asociados verificados | OK local (RNF-02 en Render: Pendiente) | Pendiente: RNF-01 en celular real |
| 3. Probada en un celular real | Pendiente | Pendiente |
| 4. Revisada por otro integrante | Pendiente (equipo de 1: revisión de código asistida + revisión propia) | Pendiente |
| 5. Registrada en informe y bitácora | OK: este archivo + `BITACORA.md` | OK |
| 6. Aceptada por el PO en la Sprint Review | Pendiente | Pendiente |
