"""
Pruebas de HU-01 · Lanzar dado (3 pts, Sprint 1)

    Como jugador, quiero lanzar un dado virtual eligiendo su tipo,
    para resolver efectos aleatorios sin un dado físico.

GUÍA DE LECTURA
- Cada test lleva en su nombre la HU y el criterio (CA) o requisito (RF/RNF)
  que verifica. Así, al correr `pytest -v`, la salida misma es la evidencia
  de la matriz de trazabilidad (docs/TRAZABILIDAD.md).
- Estas pruebas se escribieron ANTES que el código (TDD): primero fallaron,
  luego se implementó app/dominio/dado.py hasta que pasaron.
- CA2 ("se muestra en grande y reemplaza a la anterior") es de interfaz:
  aquí se prueba la parte de datos (la API devuelve solo la última tirada);
  lo visual se verifica en el celular (ver docs/TRAZABILIDAD.md).
"""
import time
from collections import Counter

import pytest
from fastapi.testclient import TestClient

from app.dominio.dado import TIPOS_DE_DADO, lanzar
from app.main import app

cliente = TestClient(app)


# ---------------------------------------------------------------------------
# CA1 · Dado que estoy en la partida, cuando elijo d6 o d20 y presiono
#       "Lanzar", entonces obtengo un valor dentro del rango de ese dado.
#       → RF-01 Lanzar dado según el tipo seleccionado
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("tipo, caras", [("d6", 6), ("d20", 20)])
def test_HU01_CA1_valor_dentro_del_rango(tipo, caras):
    # Lanzamos muchas veces: un solo lanzamiento podría "caer bien" por azar.
    for _ in range(2_000):
        valor = lanzar(tipo)
        assert 1 <= valor <= caras


@pytest.mark.parametrize("tipo, caras", [("d6", 6), ("d20", 20)])
def test_HU01_CA1_aparecen_todas_las_caras(tipo, caras):
    # Si nunca sale el 20, el rango está mal aunque ningún valor se salga.
    vistos = {lanzar(tipo) for _ in range(5_000)}
    assert vistos == set(range(1, caras + 1))


def test_HU01_CA1_tipo_de_dado_no_soportado_se_rechaza():
    # Fuera de alcance: d4, d8, d12... (no están en la HU). Se rechazan.
    with pytest.raises(ValueError):
        lanzar("d8")


def test_HU01_CA1_api_lanzar_devuelve_valor_en_rango():
    respuesta = cliente.post("/api/dado", json={"tipo": "d20"})
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["tipo"] == "d20"
    assert 1 <= datos["valor"] <= 20


def test_HU01_CA1_api_rechaza_tipo_invalido():
    respuesta = cliente.post("/api/dado", json={"tipo": "d100"})
    assert respuesta.status_code == 422  # 422 = datos de entrada inválidos


# ---------------------------------------------------------------------------
# CA2 · El resultado se muestra en grande y reemplaza a la tirada anterior.
#       → RF-02 Mostrar el resultado de la última tirada
# ---------------------------------------------------------------------------
def test_HU01_CA2_api_devuelve_un_solo_resultado_por_tirada():
    # La API responde UN valor (no una lista acumulada): la interfaz lo pinta
    # encima del anterior. El historial de tiradas es HU-03 (Sprint 2).
    datos = cliente.post("/api/dado", json={"tipo": "d6"}).json()
    assert set(datos.keys()) == {"tipo", "valor"}
    assert isinstance(datos["valor"], int)


def test_HU01_tipos_disponibles_son_d6_y_d20():
    # La interfaz arma sus botones a partir de esta lista.
    assert list(TIPOS_DE_DADO) == ["d6", "d20"]
    assert cliente.get("/api/dado/tipos").json() == ["d6", "d20"]


# ---------------------------------------------------------------------------
# RNF-02 · Rendimiento: el resultado aparece en menos de 1 s.
# ---------------------------------------------------------------------------
def test_HU01_RNF02_tirada_responde_en_menos_de_1_segundo():
    inicio = time.perf_counter()
    cliente.post("/api/dado", json={"tipo": "d20"})
    assert time.perf_counter() - inicio < 1.0


# ---------------------------------------------------------------------------
# RNF-04 · Equidad: todas las caras del dado tienen la misma probabilidad.
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("tipo, caras, n", [("d6", 6, 60_000), ("d20", 20, 100_000)])
def test_HU01_RNF04_distribucion_uniforme(tipo, caras, n):
    # Con n lanzamientos, cada cara debería salir ~n/caras veces.
    # Tolerancia del 10 %: muy por encima del ruido normal del azar
    # (≈ 1-2 %), pero detecta un dado "cargado" o un error de rango.
    conteo = Counter(lanzar(tipo) for _ in range(n))
    esperado = n / caras
    for cara in range(1, caras + 1):
        assert abs(conteo[cara] - esperado) / esperado < 0.10, (
            f"La cara {cara} salió {conteo[cara]} veces (esperado ≈{esperado:.0f})"
        )
