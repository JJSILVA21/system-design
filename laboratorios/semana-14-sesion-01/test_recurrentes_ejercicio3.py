"""Pruebas del Ejercicio 3: las escriben ustedes, en pareja, una a la vez."""
import pytest

from recurrentes_ejercicio3 import AgendaDeCancha
from reservas import CalendarioDeCancha


def test_la_agenda_reutiliza_el_calendario_por_fecha():
    agenda = AgendaDeCancha("cancha-1")
    primero = agenda.calendario("2026-11-16")
    siguiente = agenda.calendario("2026-11-23")

    assert isinstance(primero, CalendarioDeCancha)
    assert (primero.cancha, primero.fecha) == ("cancha-1", "2026-11-16")
    assert agenda.calendario("2026-11-16") is primero
    assert siguiente is not primero


def test_una_semana_reserva_la_fecha_inicial():
    agenda = AgendaDeCancha("cancha-1")

    resultado = agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, 1)

    assert resultado == [("2026-11-16", "reservada")]
    franja = agenda.calendario("2026-11-16").franja_de("entreno-1")
    assert (franja.inicio, franja.fin) == (18, 19)


def test_doce_semanas_avanzan_de_siete_en_siete_y_numeran_ids():
    agenda = AgendaDeCancha("cancha-1")
    fechas = [
        "2026-12-21", "2026-12-28", "2027-01-04", "2027-01-11",
        "2027-01-18", "2027-01-25", "2027-02-01", "2027-02-08",
        "2027-02-15", "2027-02-22", "2027-03-01", "2027-03-08",
    ]

    resultado = agenda.reservar_cada_semana("entreno", "ana", fechas[0], 18, 19, 12)

    assert resultado == [(fecha, "reservada") for fecha in fechas]
    for numero, fecha in enumerate(fechas, start=1):
        franja = agenda.calendario(fecha).franja_de(f"entreno-{numero}")
        assert (franja.inicio, franja.fin) == (18, 19)


def test_salta_la_semana_ocupada_y_conserva_la_numeracion():
    agenda = AgendaDeCancha("cancha-1")
    agenda.calendario("2026-11-23").reservar("previa", "beto", 17, 19)

    resultado = agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, 3)

    assert resultado == [
        ("2026-11-16", "reservada"),
        ("2026-11-23", "ocupada"),
        ("2026-11-30", "reservada"),
    ]
    assert agenda.calendario("2026-11-30").franja_de("entreno-3").inicio == 18


def test_salta_la_fecha_que_supera_el_limite_del_estudiante():
    agenda = AgendaDeCancha("cancha-1")
    calendario = agenda.calendario("2026-11-16")
    calendario.reservar("previa", "ana", 8, 10)
    agenda.calendario("2026-11-23").reservar("otra", "ana", 8, 9)

    resultado = agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, 2)

    assert resultado == [("2026-11-16", "limite"), ("2026-11-23", "reservada")]
    assert calendario.esta_libre(18, 19)
    assert agenda.calendario("2026-11-23").horas_de("ana") == 2


@pytest.mark.parametrize("semanas", [0, 13])
def test_rechaza_la_cantidad_de_semanas_invalida_sin_reservar(semanas):
    agenda = AgendaDeCancha("cancha-1")
    calendario = agenda.calendario("2026-11-16")

    with pytest.raises(ValueError):
        agenda.reservar_cada_semana("entreno", "ana", "2026-11-16", 18, 19, semanas)

    assert calendario.reservas() == []
