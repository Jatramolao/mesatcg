"""
Pruebas de HU-02 · Marcador de puntaje (3 pts, Sprint 1)

    Como jugador, quiero sumar y restar puntos a cada jugador,
    para saber en todo momento cómo va la partida.

GUÍA DE LECTURA
- Igual que en HU-01: nombre del test = HU + CA (+ requisito).
- Se prueba en dos niveles:
    1) dominio (clase Partida) → la regla en sí;
    2) API (/api/partidas...)  → que la regla llega igual al celular.
- El test de "nunca baja de 0" cubre el impedimento del Daily registrado
  en los antecedentes (el −1 dejaba el puntaje en negativo).
"""
import pytest
from fastapi.testclient import TestClient

from app.dominio.marcador import Partida, PartidaTerminada
from app.main import app

cliente = TestClient(app)


def crear_partida_api(j1="Ana", j2="Beto", meta=3):
    """Ayudante: crea una partida por la API y devuelve su JSON."""
    r = cliente.post("/api/partidas", json={"jugador1": j1, "jugador2": j2, "meta": meta})
    assert r.status_code == 201
    return r.json()


# ---------------------------------------------------------------------------
# CA1 · Dado que inicio una partida, cuando ingreso los dos nombres y la meta
#       de puntos, entonces ambos marcadores parten en 0.
#       → RF-03 Configurar la partida (nombres y meta)
# ---------------------------------------------------------------------------
def test_HU02_CA1_partida_nueva_parte_en_cero():
    p = Partida("Ana", "Beto", meta=10)
    assert p.nombres == ["Ana", "Beto"]
    assert p.meta == 10
    assert p.puntajes == [0, 0]
    assert p.ganador is None


def test_HU02_CA1_nombres_se_limpian_de_espacios():
    p = Partida("  Ana ", "Beto  ", meta=5)
    assert p.nombres == ["Ana", "Beto"]


@pytest.mark.parametrize("j1, j2", [("", "Beto"), ("Ana", "   ")])
def test_HU02_CA1_rechaza_nombre_vacio(j1, j2):
    with pytest.raises(ValueError):
        Partida(j1, j2, meta=5)


@pytest.mark.parametrize("meta", [0, -3])
def test_HU02_CA1_rechaza_meta_menor_a_1(meta):
    with pytest.raises(ValueError):
        Partida("Ana", "Beto", meta=meta)


def test_HU02_CA1_api_crear_partida():
    datos = crear_partida_api(meta=7)
    assert datos["nombres"] == ["Ana", "Beto"]
    assert datos["puntajes"] == [0, 0]
    assert datos["meta"] == 7
    assert datos["ganador"] is None
    assert "id" in datos  # identifica la partida de ESTA mesa


def test_HU02_CA1_api_rechaza_configuracion_invalida():
    r = cliente.post("/api/partidas", json={"jugador1": "", "jugador2": "Beto", "meta": 5})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# CA2 · +1 y −1 modifican el puntaje, y nunca baja de 0.
#       → RF-04 Sumar y restar puntos, con mínimo 0
# ---------------------------------------------------------------------------
def test_HU02_CA2_sumar_y_restar_modifican_el_puntaje():
    p = Partida("Ana", "Beto", meta=10)
    p.sumar(0)
    p.sumar(0)
    p.sumar(1)
    p.restar(0)
    assert p.puntajes == [1, 1]


def test_HU02_CA2_restar_nunca_baja_de_cero():
    # Impedimento del Daily: el −1 dejaba el puntaje bajo 0.
    p = Partida("Ana", "Beto", meta=10)
    p.restar(0)
    p.restar(0)
    assert p.puntajes == [0, 0]


def test_HU02_CA2_jugador_inexistente_se_rechaza():
    p = Partida("Ana", "Beto", meta=10)
    with pytest.raises(IndexError):
        p.sumar(2)


def test_HU02_CA2_api_sumar_y_restar():
    pid = crear_partida_api(meta=10)["id"]
    cliente.post(f"/api/partidas/{pid}/jugadores/1/sumar")
    cliente.post(f"/api/partidas/{pid}/jugadores/1/sumar")
    datos = cliente.post(f"/api/partidas/{pid}/jugadores/1/restar").json()
    assert datos["puntajes"] == [0, 1]


def test_HU02_CA2_api_restar_nunca_baja_de_cero():
    pid = crear_partida_api()["id"]
    datos = cliente.post(f"/api/partidas/{pid}/jugadores/0/restar").json()
    assert datos["puntajes"] == [0, 0]


def test_HU02_CA2_api_jugador_o_partida_inexistente_da_404():
    pid = crear_partida_api()["id"]
    assert cliente.post(f"/api/partidas/{pid}/jugadores/5/sumar").status_code == 404
    assert cliente.post("/api/partidas/no-existe/jugadores/0/sumar").status_code == 404


# ---------------------------------------------------------------------------
# CA3 · Cuando un jugador alcanza la meta, la app indica quién ganó.
#       → RF-05 Detectar y anunciar al ganador
# ---------------------------------------------------------------------------
def test_HU02_CA3_al_alcanzar_la_meta_hay_ganador():
    p = Partida("Ana", "Beto", meta=2)
    p.sumar(1)
    assert p.ganador is None  # aún no llega
    p.sumar(1)
    assert p.ganador == "Beto"


def test_HU02_CA3_con_ganador_el_marcador_queda_congelado():
    # Decisión de diseño (ver docs/TRAZABILIDAD.md): una vez que hay ganador,
    # no se aceptan más cambios, para que el resultado no se altere por error.
    p = Partida("Ana", "Beto", meta=1)
    p.sumar(0)
    with pytest.raises(PartidaTerminada):
        p.sumar(1)
    with pytest.raises(PartidaTerminada):
        p.restar(0)
    assert p.puntajes == [1, 0]
    assert p.ganador == "Ana"


def test_HU02_CA3_api_anuncia_ganador_y_bloquea_cambios():
    pid = crear_partida_api(j1="Ana", j2="Beto", meta=2)["id"]
    cliente.post(f"/api/partidas/{pid}/jugadores/0/sumar")
    datos = cliente.post(f"/api/partidas/{pid}/jugadores/0/sumar").json()
    assert datos["ganador"] == "Ana"
    r = cliente.post(f"/api/partidas/{pid}/jugadores/1/sumar")
    assert r.status_code == 409  # 409 = conflicto: la partida ya terminó


def test_HU02_partidas_de_distintas_mesas_no_se_mezclan():
    # Si dos mesas usan la app a la vez, cada una tiene su propia partida.
    a = crear_partida_api()["id"]
    b = crear_partida_api()["id"]
    cliente.post(f"/api/partidas/{a}/jugadores/0/sumar")
    assert cliente.get(f"/api/partidas/{b}").json()["puntajes"] == [0, 0]
