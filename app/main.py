"""
API · MesaTCG (Sprint 1)
========================
Capa que conecta la interfaz (app/static/index.html) con la lógica
(app/dominio/). No contiene reglas del juego: solo recibe peticiones,
llama al dominio y responde en JSON.

Endpoints del Sprint 1
- GET  /                          → sirve la interfaz (RNF-03: solo navegador)
- GET  /static/...                → fuentes y archivos de la interfaz
- GET  /api/dado/tipos            → HU-01 · tipos disponibles (d6, d20)
- POST /api/dado                  → HU-01 · CA1/CA2 · lanzar dado
- POST /api/partidas              → HU-02 · CA1 · crear partida (nombres + meta)
- GET  /api/partidas/{id}         → HU-02 · ver estado del marcador
- POST /api/partidas/{id}/jugadores/{0|1}/{sumar|restar}
                                  → HU-02 · CA2 (+1/−1, mínimo 0) · CA3 (ganador)

Ejecutar en local:   uvicorn app.main:app --reload
Documentación viva:  http://127.0.0.1:8000/docs  (la genera FastAPI)
"""
from pathlib import Path
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.dominio.dado import TIPOS_DE_DADO, lanzar
from app.dominio.marcador import Partida, PartidaTerminada

app = FastAPI(title="MesaTCG", version="0.1.0")

CARPETA_STATIC = Path(__file__).parent / "static"

# Archivos estáticos (fuentes autoalojadas en /static/fonts/).
# Se sirven desde el mismo servidor: la app no depende de Google Fonts.
app.mount("/static", StaticFiles(directory=CARPETA_STATIC), name="static")


# ---------------------------------------------------------------------------
# Interfaz
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
def interfaz():
    # RNF-03 · Portabilidad: el jugador solo abre la URL en el celular.
    return FileResponse(CARPETA_STATIC / "index.html")


# ---------------------------------------------------------------------------
# HU-01 · Lanzar dado
# ---------------------------------------------------------------------------
class PedidoTirada(BaseModel):
    # Literal hace que FastAPI rechace (422) cualquier tipo fuera del alcance.
    tipo: Literal["d6", "d20"]


class ResultadoTirada(BaseModel):
    tipo: str
    valor: int


@app.get("/api/dado/tipos")
def tipos_de_dado() -> list[str]:
    return list(TIPOS_DE_DADO)


@app.post("/api/dado")
def lanzar_dado(pedido: PedidoTirada) -> ResultadoTirada:
    # CA1 / RF-01 · el valor depende del tipo elegido.
    # CA2 / RF-02 · se devuelve SOLO esta tirada; la interfaz reemplaza
    #               la anterior. No se guarda nada (el historial es HU-03).
    return ResultadoTirada(tipo=pedido.tipo, valor=lanzar(pedido.tipo))


# ---------------------------------------------------------------------------
# HU-02 · Marcador de puntaje
# ---------------------------------------------------------------------------
# ALMACENAMIENTO DEL SPRINT 1: un diccionario en memoria {id: Partida}.
# - Cada mesa recibe un id propio, así dos mesas no se pisan el marcador.
# - Si el servidor se reinicia, las partidas se pierden: es ESPERADO en este
#   sprint. Conservar la partida es HU-03 / RF-07 (Sprint 2, con MongoDB):
#   ahí este diccionario se reemplaza por una colección `partidas`.
partidas: dict[str, Partida] = {}


class PedidoPartida(BaseModel):
    # Validación de entrada (CA1 / RF-03): nombres no vacíos, meta >= 1.
    # El dominio vuelve a validar: la API filtra lo obvio, el dominio manda.
    jugador1: str = Field(min_length=1, max_length=30)
    jugador2: str = Field(min_length=1, max_length=30)
    meta: int = Field(ge=1, le=999)


def _respuesta(pid: str, partida: Partida) -> dict:
    return {"id": pid, **partida.a_dict()}


def _buscar(pid: str) -> Partida:
    if pid not in partidas:
        raise HTTPException(404, "Partida no encontrada")
    return partidas[pid]


@app.post("/api/partidas", status_code=201)
def crear_partida(pedido: PedidoPartida) -> dict:
    # CA1 · se crea con ambos marcadores en 0.
    try:
        partida = Partida(pedido.jugador1, pedido.jugador2, pedido.meta)
    except ValueError as error:  # p. ej. nombre de solo espacios
        raise HTTPException(422, str(error))
    pid = uuid4().hex
    partidas[pid] = partida
    return _respuesta(pid, partida)


@app.get("/api/partidas/{pid}")
def ver_partida(pid: str) -> dict:
    return _respuesta(pid, _buscar(pid))


@app.post("/api/partidas/{pid}/jugadores/{jugador}/{accion}")
def cambiar_puntaje(pid: str, jugador: int, accion: Literal["sumar", "restar"]) -> dict:
    # CA2 / RF-04 · +1 o −1 (el mínimo 0 lo garantiza el dominio).
    # CA3 / RF-05 · la respuesta incluye "ganador" para que la interfaz lo anuncie.
    partida = _buscar(pid)
    try:
        getattr(partida, accion)(jugador)  # llama a partida.sumar() o partida.restar()
    except IndexError:
        raise HTTPException(404, "Jugador inexistente")
    except PartidaTerminada as error:
        raise HTTPException(409, str(error))
    return _respuesta(pid, partida)
