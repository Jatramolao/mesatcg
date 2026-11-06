# MesaTCG

App web para el celular que reúne **dado**, **marcador** e **historial** para partidas presenciales de TCG (Riftbound, Mitos y Leyendas).

> Proyecto de ejemplo docente · **RQY1101 Ingeniería de Requisitos** · Duoc UC
> Un solo integrante (el docente) ejerce los roles de Product Owner, Scrum Master y Developer. En un equipo real esos roles están separados.

| | |
|---|---|
| **Versión actual** | `v0.1.0`: incremento del Sprint 1 (HU-01 + HU-02) |
| **Estado** | Sprint 1 implementado · 34/34 pruebas en verde · pendiente: celular real y Sprint Review |
| **Trazabilidad detallada** | [`docs/TRAZABILIDAD.md`](docs/TRAZABILIDAD.md) |
| **Bitácora** | [`docs/BITACORA.md`](docs/BITACORA.md) |

---

## 1. Plan de proyecto

### 1.1 Necesidad de origen (épica)

Historia tal como llegó del cliente:

> "Como jugador de TCG como Riftbound o Mitos y Leyendas, necesito disponer de una forma para disponer de un dado y marcador de puntaje, para no perder los antecedentes de mi partida."

Épica refinada:

> **Como** jugador de TCG presencial (Riftbound, Mitos y Leyendas), **quiero** una herramienta en mi celular que reúna dado, marcador e historial de la partida, **para** jugar sin papel ni dados físicos y sin perder el registro de lo que pasó.

### 1.2 Visión

Para jugadores de TCG presencial que hoy usan dados físicos y papel, **MesaTCG** es una app web para el celular que reúne dado, marcador e historial. A diferencia del papel, el registro de la partida no se pierde.

### 1.3 Product Goal

> Que los jugadores de TCG presencial puedan llevar una partida completa desde el celular, sin dados ni papel, y sin perder el registro de lo que pasó.

---

## 2. Product Backlog priorizado

| Prioridad | Historia | Pts | Sprint | Estado |
|---|---|---|---|---|
| 1 | HU-01 Lanzar dado | 3 | **Sprint 1** | Implementada |
| 2 | HU-02 Marcador de puntaje | 3 | **Sprint 1** | Implementada |
| 3 | HU-03 Historial y conservación de la partida | 5 | Sprint 2 | Planificada |
| 4 | HU-04 Contadores adicionales (recursos, turnos) | s/e | Por refinar | Emergente |
| 5 | HU-05 Temporizador de turno | s/e | Por refinar | Emergente |

HU-04 y HU-05 quedan sin estimar (s/e) a propósito: el backlog es **DEEP** (detallado arriba, emergente abajo).

---

## 3. Historias de usuario

### HU-01 · Lanzar dado (3 pts · Sprint 1)

> **Como** jugador, **quiero** lanzar un dado virtual eligiendo su tipo, **para** resolver efectos aleatorios sin un dado físico.

- **CA1:** Dado que estoy en la partida, cuando elijo d6 o d20 y presiono "Lanzar", entonces obtengo un valor dentro del rango de ese dado.
- **CA2:** El resultado se muestra en grande y reemplaza a la tirada anterior.

### HU-02 · Marcador de puntaje (3 pts · Sprint 1)

> **Como** jugador, **quiero** sumar y restar puntos a cada jugador, **para** saber en todo momento cómo va la partida.

- **CA1:** Dado que inicio una partida, cuando ingreso los dos nombres y la meta de puntos, entonces ambos marcadores parten en 0.
- **CA2:** +1 y −1 modifican el puntaje, y nunca baja de 0.
- **CA3:** Cuando un jugador alcanza la meta, la app indica quién ganó.

### HU-03 · Historial y conservación de la partida (5 pts · Sprint 2)

> **Como** jugador, **quiero** ver el registro de la partida y que no se borre, **para** revisar jugadas en caso de duda y no perder el avance.

- **CA1:** Cada cambio de puntaje y cada tirada se registra con hora, jugador y valor.
- **CA2:** Si cierro o recargo la app, la partida sigue tal como estaba.
- **CA3:** Para "Nueva partida" la app pide confirmación antes de borrar el historial.

### HU-04 · Contadores adicionales · HU-05 · Temporizador de turno

Por refinar y estimar según el feedback de la Sprint Review del Sprint 1.

---

## 4. Requisitos derivados

| ID | Requisito | HU | Sprint |
|---|---|---|---|
| RF-01 | Lanzar dado según el tipo seleccionado (d6, d20) | HU-01 | 1 |
| RF-02 | Mostrar el resultado de la última tirada | HU-01 | 1 |
| RF-03 | Configurar la partida (nombres y meta) | HU-02 | 1 |
| RF-04 | Sumar y restar puntos, con mínimo 0 | HU-02 | 1 |
| RF-05 | Detectar y anunciar al ganador | HU-02 | 1 |
| RF-06 | Registrar el historial de tiradas y puntajes | HU-03 | 2 |
| RF-07 | Conservar la partida al cerrar o recargar | HU-03 | 2 |
| RNF-01 | Usabilidad: botones operables con una mano y resultado legible a 1 m | HU-01, HU-02 | 1 |
| RNF-02 | Rendimiento: el resultado aparece en menos de 1 s | HU-01 | 1 |
| RNF-03 | Portabilidad: funciona en el navegador del celular sin instalar nada | Todas | 1 |
| RNF-04 | Equidad: todas las caras del dado tienen la misma probabilidad | HU-01 | 1 |

---

## 5. Sprints

### Sprint 1: Dado y marcador (implementado)

- **Sprint Goal:** que dos jugadores puedan resolver tiradas y llevar el puntaje de su partida desde un celular.
- **Sprint Backlog:** HU-01 + HU-02 = **6 pts**. HU-03 queda fuera porque introduce la capa de datos.
- **Incremento:** dado y marcador usables desde el navegador del celular.
- **Fuera de alcance:** persistencia, historial, cuentas de usuario, juego en línea.
- **Métricas de éxito:** se juega una partida completa sin dado ni papel · la tirada responde en menos de 1 s · el PO acepta HU-01 y HU-02.

| Evento | Registro |
|---|---|
| Sprint Planning | De aquí salieron el Sprint Goal y el Sprint Backlog |
| Planning Poker | HU-02 recibió votos 2, 3 y 5; se acordó 3 |
| Daily (impedimento) | El −1 dejaba el puntaje bajo 0. Se resolvió con una prueba escrita antes que el código |
| Sprint Review | *Pendiente* (en el guion: el PO pide el resultado del dado más grande y eso ajusta RNF-01) |
| Retrospective | *Pendiente* (mejora prevista: probar en el celular desde el día 1) |

### Sprint 2: Historial y conservación (planificado)

- **Sprint Goal (propuesto):** que la partida y su registro sobrevivan a cerrar o recargar la app.
- **Sprint Backlog:** HU-03 = **5 pts**.
- **Cambios técnicos:** entra **MongoDB Atlas**, con dos colecciones:
  - `partidas`: `{nombres, meta, puntajes, ganador}`
  - `eventos`: `{partida_id, hora, jugador, tipo, valor}`, una entrada por cada tirada o cambio de puntaje.
- **Con esto se completa el MVP** (HU-01 a HU-03).

### Sprint 3 en adelante (emergente)

Refinar, estimar y priorizar HU-04 y HU-05 según el feedback de la Review del Sprint 1.

### MVP

**MVP = HU-01 + HU-02 + HU-03.** Se alcanza al cerrar el Sprint 2.

---

## 6. Definition of Done (aplica a toda historia)

1. Cumple todos sus criterios de aceptación.
2. Sus RNF asociados están verificados.
3. Está probada en un celular real.
4. Otro integrante la revisó.
5. Está registrada en el informe (HU, RF/RNF, trazabilidad) y en la bitácora.
6. El Product Owner la aceptó en la Sprint Review.

> Los criterios de aceptación son propios de cada historia; la DoD es la misma para todas.

---

## 7. Stack tecnológico

| Capa | Sprint 1 | Sprint 2 |
|---|---|---|
| Lógica (reglas del juego) | Python 3.12 puro → `app/dominio/` | igual |
| API | FastAPI + Uvicorn → `app/main.py` | + `pymongo` |
| Datos | En memoria (se pierde al reiniciar: es lo esperado) | MongoDB Atlas (M0 gratis) |
| Interfaz | HTML + CSS + JS sin dependencias → `app/static/index.html` | + vista de historial |
| Pruebas | pytest: un test por criterio de aceptación | + pruebas de persistencia |
| Hosting | Render | Render + Atlas |

### Diseño visual

Campo de batalla medieval, con lenguaje brutalista. Es inspiración de género; no usa elementos de ninguna franquicia.

- **Tipografía:** Grenze Gotisch (gótica) solo en el título y el anuncio del ganador. Big Shoulders Stencil (estarcido militar) para números, nombres y botones. Las dos tienen licencia OFL y están autoalojadas en `app/static/fonts/`, con su licencia al lado.
- **Color:** hierro y hollín de base, con un solo acento color brasa. Tema oscuro único, pensado para mesas con luz baja.
- **Forma:** esquinas biseladas como placas de armadura, sin bordes redondeados.
- **Legibilidad (RNF-01):** botones de 64 px, puntaje de 96 px y dado de 160 px.

**¿Por qué Python y no un solo `index.html`?** Es el stack que domina el equipo y permite verificar cada criterio de aceptación con una prueba automatizada que lleva su nombre (`test_HU02_CA2_restar_nunca_baja_de_cero`). Las reglas viven solo en Python; la interfaz únicamente muestra lo que responde la API.

### Estructura

```
app/
  dominio/dado.py        HU-01 · RF-01, RNF-04
  dominio/marcador.py    HU-02 · RF-03, RF-04, RF-05
  main.py                API: conecta interfaz ↔ dominio
  static/index.html      interfaz · RF-02, RNF-01, RNF-03
  static/fonts/          fuentes autoalojadas + licencias OFL
tests/
  test_hu01_dado.py      verifica HU-01 (CA1, CA2, RNF-02, RNF-04)
  test_hu02_marcador.py  verifica HU-02 (CA1, CA2, CA3)
  test_interfaz.py       verifica RNF-03 (página y fuentes sin servicios externos)
docs/
  TRAZABILIDAD.md        HU → CA → código → prueba → estado
  BITACORA.md            registro por sesión (Daily, impedimentos, uso de IA)
render.yaml              configuración de despliegue en Render
```

---

## 8. Cómo ejecutar

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
pytest                                           # 34 pruebas, cada una con su HU y CA
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

- Computador: http://localhost:8000
- Celular (misma red wifi): `http://<IP-del-computador>:8000`
- Documentación interactiva de la API: http://localhost:8000/docs

### Desplegar en Render

1. En Render: **New → Blueprint** y elegir este repositorio (Render lee `render.yaml`).
2. Abrir la URL un minuto antes de la demo: en el plan gratuito el servidor se duerme tras unos 15 minutos sin uso.

---

## 9. Guion de demo (orden de la matriz de trazabilidad)

1. **HU-02 CA1:** ingresar "Ana", "Beto" y la meta 3 → el marcador parte en 0 a 0.
2. **HU-01 CA1:** elegir d6 y lanzar; luego d20 y lanzar → el valor queda en rango.
3. **HU-01 CA2:** lanzar varias veces → el número grande se reemplaza.
4. **HU-02 CA2:** pulsar −1 con el marcador en 0 → sigue en 0.
5. **HU-02 CA3:** sumar hasta la meta → aparece "¡Ganó Beto!" y el marcador se bloquea.
6. Mostrar `pytest` con las 34 pruebas en verde.

---

## 10. Uso declarado de IA

- **Qué se hizo con IA:** el código (dominio, API, interfaz y pruebas) se generó con Claude Code a partir de las HU y sus criterios de aceptación.
- **Qué se corrigió:** el stack del plan original (un solo `index.html` en JS) se cambió a Python + FastAPI. El caso del −1 bajo 0 quedó cubierto con una prueba antes de escribir el código.
- **Qué se descartó:** cuentas de usuario y juego en línea (fuera del Sprint Goal), y la persistencia en el Sprint 1 (adelantaría HU-03).
