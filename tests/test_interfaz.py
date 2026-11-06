"""
Pruebas de la interfaz · RNF-03 Portabilidad

Verifica que el servidor entrega la página y las fuentes autoalojadas.
Las fuentes viven en app/static/fonts/ para que la app no dependa de
servicios externos (Google Fonts) al cargar en el celular.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_RNF03_la_pagina_se_sirve_en_la_raiz():
    r = cliente.get("/")
    assert r.status_code == 200
    assert "text/html" in r.headers["content-type"]


@pytest.mark.parametrize("fuente", ["grenze-gotisch.woff2", "big-shoulders-stencil.woff2"])
def test_RNF03_fuentes_autoalojadas_disponibles(fuente):
    r = cliente.get(f"/static/fonts/{fuente}")
    assert r.status_code == 200
    assert r.content[:4] == b"wOF2"  # firma de un archivo WOFF2 real


def test_RNF03_la_pagina_no_depende_de_servicios_externos():
    html = cliente.get("/").text
    assert "fonts.googleapis.com" not in html
    assert "cdn." not in html
