# MesaTCG · Bitácora del Sprint 1

Registro cronológico de lo hecho, los impedimentos y el uso de IA. Agrega una entrada por cada sesión de trabajo (equivale al Daily).

---

## 2026-11-05 · Sesión 1: arranque e implementación

**Decisión de stack.** El documento de antecedentes pedía un solo `index.html` en JS. Se cambió a **Python (FastAPI) + pytest**, porque es el stack que domina el equipo y porque permite verificar cada CA con un test automatizado. **MongoDB** queda para el Sprint 2 (HU-03), cuando la capa de datos entra al alcance. El hosting pasa de GitHub Pages/Netlify a **Render**, porque esos servicios no ejecutan Python.

**Hecho**
- Estructura del proyecto, entorno Python 3.12, dependencias.
- HU-01: primero las pruebas (12 tests en rojo), luego `dado.py` y `POST /api/dado` → en verde.
- HU-02: primero las pruebas (18 tests), luego `marcador.py` y los endpoints de partida → en verde.
- Interfaz mobile-first: configuración, marcador y panel de dado.
- Verificación en el navegador en vista móvil (375×812): los 5 CA se demuestran en pantalla.
- Resultado: **30/30 pruebas en verde**.

**Impedimento (Daily).** El impedimento registrado en los antecedentes ("el −1 dejaba el puntaje bajo 0", que no cumplía HU-02 CA2) se previno escribiendo primero su prueba, `test_HU02_CA2_restar_nunca_baja_de_cero`, y resolviéndolo con `max(0, puntaje − 1)`. En esta implementación la prueba nunca falló por esa causa.

**Uso de IA**
- *Con IA:* el código inicial de dominio, API, interfaz y pruebas se generó con Claude Code a partir de las HU y sus CA.
- *Corregido:* stack del documento original (JS → Python) y redacción de la bitácora. El caso del −1 quedó cubierto por una prueba antes de escribir el código.
- *Descartado:* cuentas de usuario y juego en línea (fuera del Sprint Goal). También el guardado en `localStorage` o MongoDB, porque adelantaría HU-03.

**Pendiente**
- [ ] Probar en un celular real (DoD 3, RNF-01, RNF-03).
- [ ] Desplegar en Render y medir RNF-02 en producción.
- [ ] Actualizar la sección 13 del documento de antecedentes con el nuevo stack.
- [ ] Sprint Review con el PO.
