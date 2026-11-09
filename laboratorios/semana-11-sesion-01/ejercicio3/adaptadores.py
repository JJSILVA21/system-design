"""Los adaptadores de la cancelacion. RelojDelSistema y NotificadorPorCorreo
ya estan completos; los demas son tuyos."""

import sqlite3
import time

import correo_simulado
from dominio import Reserva
from puertos import Notificador, Reloj, RepositorioDeReservas


class RepositorioSqlite(RepositorioDeReservas):
    # TODO 3: el SQL de cancelaciones_acopladas.py, movido aqui: las dos
    # tablas en el constructor, y un metodo por cada metodo del puerto.
    # El id que devuelve y recibe es "r-" seguido del numero de SQLite.
    def __init__(self, ruta_base_de_datos):
        self.conexion = sqlite3.connect(ruta_base_de_datos)

        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS reservas ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "estudiante TEXT, cancha TEXT, fecha TEXT, hora INTEGER)"
        )

        self.conexion.execute(
            "CREATE TABLE IF NOT EXISTS penalizaciones "
            "(estudiante TEXT)"
        )

    def agregar(self, estudiante, cancha, fecha, hora):
        cursor = self.conexion.execute(
            "INSERT INTO reservas "
            "(estudiante, cancha, fecha, hora) "
            "VALUES (?, ?, ?, ?)",
            (estudiante, cancha, fecha, hora),
        )

        self.conexion.commit()

        return Reserva(
            "r-" + str(cursor.lastrowid),
            estudiante,
            cancha,
            fecha,
            hora,
        )

    def buscar(self, id_reserva):
        numero = int(id_reserva[2:])

        fila = self.conexion.execute(
            "SELECT estudiante, cancha, fecha, hora "
            "FROM reservas WHERE id = ?",
            (numero,),
        ).fetchone()

        if fila is None:
            return None

        return Reserva(
            id_reserva,
            fila[0],
            fila[1],
            fila[2],
            fila[3],
        )

    def borrar(self, id_reserva):
        numero = int(id_reserva[2:])

        self.conexion.execute(
            "DELETE FROM reservas WHERE id = ?",
            (numero,),
        )

        self.conexion.commit()

    def registrar_penalizacion(self, estudiante):
        self.conexion.execute(
            "INSERT INTO penalizaciones (estudiante) VALUES (?)",
            (estudiante,),
        )

        self.conexion.commit()

    def penalizaciones_de(self, estudiante):
        fila = self.conexion.execute(
            "SELECT COUNT(*) FROM penalizaciones "
            "WHERE estudiante = ?",
            (estudiante,),
        ).fetchone()

        return fila[0]


class RepositorioEnMemoria(RepositorioDeReservas):
    # TODO 4: el mismo puerto sobre diccionarios, con ids "r-1", "r-2", ...
    def __init__(self):
        self.reservas = {}
        self.siguiente_numero = 1
        self.penalizaciones = []

    def agregar(self, estudiante, cancha, fecha, hora):
        id_reserva = "r-" + str(self.siguiente_numero)
        self.siguiente_numero = self.siguiente_numero + 1

        reserva = Reserva(
            id_reserva,
            estudiante,
            cancha,
            fecha,
            hora,
        )

        self.reservas[id_reserva] = reserva
        return reserva

    def buscar(self, id_reserva):
        return self.reservas.get(id_reserva)

    def borrar(self, id_reserva):
        self.reservas.pop(id_reserva, None)

    def registrar_penalizacion(self, estudiante):
        self.penalizaciones.append(estudiante)

    def penalizaciones_de(self, estudiante):
        cantidad = 0

        for penalizado in self.penalizaciones:
            if penalizado == estudiante:
                cantidad = cantidad + 1

        return cantidad


class RelojFijo(Reloj):
    # TODO 5: un reloj que siempre devuelve la fecha y la hora que recibio
    # al construirse: RelojFijo("2026-11-10", 16).
    def __init__(self, fecha, hora):
        self.fecha = fecha
        self.hora = hora

    def ahora(self):
        return (self.fecha, self.hora)


class RelojDelSistema(Reloj):
    def ahora(self):
        return (
            time.strftime("%Y-%m-%d"),
            time.localtime().tm_hour,
        )


class NotificadorEnMemoria(Notificador):
    # TODO 6: guarda cada notificacion en self.enviados como una tupla
    # (estudiante, mensaje).
    def __init__(self):
        self.enviados = []

    def notificar(self, estudiante, mensaje):
        self.enviados.append((estudiante, mensaje))


class NotificadorPorCorreo(Notificador):
    def notificar(self, estudiante, mensaje):
        correo_simulado.enviar_correo(estudiante, mensaje)