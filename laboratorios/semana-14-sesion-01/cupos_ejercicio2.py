"""Ejercicio 2: el cupo semanal de reservas, con TDD.

ReservaU limita cuantas reservas puede tener cada estudiante por semana,
para que nadie acapare las canchas. La regla:

- Cada estudiante puede tener como maximo 3 reservas activas por semana.
  La semana va de lunes a domingo (semana_de, abajo, ya lo resuelve).
- Las reservas de semanas distintas no se suman.
- Cancelar una reserva libera su lugar en el cupo.
- Los equipos oficiales registrados tienen un cupo de 6.
- Registrar una reserva cuando el cupo esta agotado lanza
  ValueError("cupo semanal agotado"), y no la registra.

La clase se llama CupoSemanal y tiene, al final, estos metodos:

- puede_reservar(estudiante, fecha): True si le queda cupo esa semana.
- registrar(id_reserva, estudiante, fecha)
- cancelar(id_reserva)
- registrar_equipo_oficial(estudiante)

La lista de pruebas esta en test_cupos_ejercicio2.py. La primera ya esta
escrita. Corre las pruebas con:

    pytest test_cupos_ejercicio2.py

Cuando termines la lista, y no antes, corre las pruebas de aceptacion:

    pytest test_aceptacion_cupos.py
"""

from datetime import date


def semana_de(fecha):
    anio, semana, _ = date.fromisoformat(fecha).isocalendar()
    return (anio, semana)


class CupoSemanal:
    def __init__(self):
        self._reservas = {}
        self._equipos_oficiales = set()

    def puede_reservar(self, estudiante, fecha):
        semana = semana_de(fecha)
        activas = 0
        for titular, semana_reserva in self._reservas.values():
            if titular == estudiante and semana_reserva == semana:
                activas += 1
        limite = 3
        if estudiante in self._equipos_oficiales:
            limite = 6
        return activas < limite

    def registrar(self, id_reserva, estudiante, fecha):
        if not self.puede_reservar(estudiante, fecha):
            raise ValueError("cupo semanal agotado")
        self._reservas[id_reserva] = (estudiante, semana_de(fecha))

    def cancelar(self, id_reserva):
        if id_reserva not in self._reservas:
            raise ValueError("reserva desconocida")
        del self._reservas[id_reserva]

    def registrar_equipo_oficial(self, estudiante):
        self._equipos_oficiales.add(estudiante)

