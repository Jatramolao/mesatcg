"""
Dominio · Marcador de puntaje
=============================
Implementa: HU-02 Marcador de puntaje
Requisitos: RF-03 (configurar) · RF-04 (sumar/restar, mínimo 0) · RF-05 (ganador)
Pruebas:    tests/test_hu02_marcador.py

GUÍA
- `Partida` concentra TODAS las reglas del marcador. La API y la interfaz
  no deciden nada: si mañana cambia una regla, se cambia solo aquí.
- Los jugadores se identifican por posición: 0 = jugador 1, 1 = jugador 2.
- Sprint 2 (HU-03): esta clase se guardará en MongoDB como un documento
  {nombres, meta, puntajes, ganador} y cada sumar/restar generará un evento
  del historial. Por eso el estado se mantiene en atributos simples.
"""

PUNTAJE_MINIMO = 0  # RF-04 · el puntaje nunca baja de este valor


class PartidaTerminada(Exception):
    """Se intentó modificar el puntaje cuando ya hay un ganador."""


class Partida:
    def __init__(self, jugador1: str, jugador2: str, meta: int):
        # --- CA1 / RF-03 · configurar partida -------------------------------
        nombres = [jugador1.strip(), jugador2.strip()]
        if not all(nombres):
            raise ValueError("Ambos jugadores deben tener nombre")
        if meta < 1:
            raise ValueError("La meta debe ser al menos 1 punto")

        self.nombres: list[str] = nombres
        self.meta: int = meta
        self.puntajes: list[int] = [0, 0]  # CA1 · ambos marcadores parten en 0

    # --- CA3 / RF-05 · detectar ganador --------------------------------------
    @property
    def ganador(self) -> str | None:
        """Nombre de quien alcanzó la meta, o None si la partida sigue.

        Se calcula a partir de los puntajes (no se guarda aparte), así nunca
        puede quedar "desincronizado" del marcador.
        Como el marcador se congela al primer ganador (ver _validar_cambio),
        nunca puede haber dos jugadores en la meta al mismo tiempo.
        """
        for nombre, puntaje in zip(self.nombres, self.puntajes):
            if puntaje >= self.meta:
                return nombre
        return None

    # --- CA2 / RF-04 · sumar y restar ----------------------------------------
    def sumar(self, jugador: int) -> None:
        self._validar_cambio(jugador)
        self.puntajes[jugador] += 1

    def restar(self, jugador: int) -> None:
        self._validar_cambio(jugador)
        # max(...) resuelve el impedimento del Daily: con un simple "-= 1"
        # el puntaje quedaría negativo y no cumpliría HU-02 CA2.
        self.puntajes[jugador] = max(PUNTAJE_MINIMO, self.puntajes[jugador] - 1)

    def _validar_cambio(self, jugador: int) -> None:
        """Reglas comunes antes de tocar un puntaje."""
        if jugador not in (0, 1):
            raise IndexError(f"Jugador inexistente: {jugador}")
        # Decisión de diseño: con ganador, el marcador queda congelado para
        # que el resultado anunciado (CA3) no cambie por un toque accidental.
        # Para jugar otra, se crea una partida nueva.
        if self.ganador is not None:
            raise PartidaTerminada(f"La partida terminó: ganó {self.ganador}")

    # --- Salida para la API ---------------------------------------------------
    def a_dict(self) -> dict:
        return {
            "nombres": self.nombres,
            "meta": self.meta,
            "puntajes": self.puntajes,
            "ganador": self.ganador,
        }
