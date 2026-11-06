"""
Dominio · Dado virtual
======================
Implementa: HU-01 Lanzar dado
Requisitos: RF-01 (lanzar según tipo) · RNF-04 (equidad)
Pruebas:    tests/test_hu01_dado.py

GUÍA
- Este módulo es "lógica pura": no sabe nada de web ni de pantallas.
  Por eso se puede probar directamente y se reutiliza igual en el Sprint 2.
- La API (app/main.py) llama a `lanzar()` y la interfaz solo muestra el valor.
"""
import secrets

# Tipos de dado del alcance de HU-01 (CA1 menciona solo d6 y d20).
# Clave = nombre que ve el jugador; valor = cantidad de caras.
# ¿Agregar d4, d8, d12? Sería una historia nueva o un refinamiento de HU-01:
# no se agregan "porque sí" (evita alcance no pedido).
TIPOS_DE_DADO: dict[str, int] = {
    "d6": 6,
    "d20": 20,
}


def lanzar(tipo: str) -> int:
    """Lanza un dado del tipo indicado y devuelve un valor entre 1 y sus caras.

    RF-01 · el rango depende del tipo seleccionado.
    RNF-04 · equidad: usamos `secrets.randbelow`, que obtiene el azar del
    sistema operativo (criptográficamente seguro) y es uniforme: cada cara
    tiene exactamente la misma probabilidad. Es el equivalente en Python de
    `crypto.getRandomValues` que pedía el documento original.
    (`random.randint` también sería uniforme, pero es predecible; para un
    dado de juego preferimos la fuente más robusta.)

    Lanza ValueError si el tipo no está en TIPOS_DE_DADO.
    """
    if tipo not in TIPOS_DE_DADO:
        raise ValueError(f"Tipo de dado no soportado: {tipo!r}")

    caras = TIPOS_DE_DADO[tipo]
    # randbelow(caras) entrega 0..caras-1  →  sumamos 1 para obtener 1..caras
    return secrets.randbelow(caras) + 1
