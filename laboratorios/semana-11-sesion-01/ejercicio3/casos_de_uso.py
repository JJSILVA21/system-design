"""El caso de uso de cancelar una reserva. Solo puede importar dominio."""

from dominio import clasificar_cancelacion


class CancelarReserva:
    def __init__(self, repositorio, reloj, notificador):
        self.repositorio = repositorio
        self.reloj = reloj
        self.notificador = notificador

    def ejecutar(self, id_reserva, estudiante):
        # TODO 2: el mismo flujo de ServicioDeCancelaciones.cancelar, con los
        # mismos resultados y los mismos mensajes, usando solo los tres
        # puertos y clasificar_cancelacion.
        reserva = self.repositorio.buscar(id_reserva)

        if reserva is None:
            return {
                "estado": "rechazada",
                "motivo": "reserva desconocida",
            }

        if reserva.estudiante != estudiante:
            return {
                "estado": "rechazada",
                "motivo": "no es tu reserva",
            }

        fecha_actual, hora_actual = self.reloj.ahora()

        clasificacion = clasificar_cancelacion(
            reserva.fecha,
            reserva.hora,
            fecha_actual,
            hora_actual,
        )

        if clasificacion == "vencida":
            return {
                "estado": "rechazada",
                "motivo": "la reserva ya empezo",
            }

        tardia = clasificacion == "tardia"

        self.repositorio.borrar(id_reserva)

        if tardia:
            self.repositorio.registrar_penalizacion(estudiante)
            mensaje = (
                "Reserva "
                + id_reserva
                + " cancelada con penalizacion por aviso tardio"
            )
        else:
            mensaje = "Reserva " + id_reserva + " cancelada"

        self.notificador.notificar(
            estudiante,
            mensaje,
        )

        return {
            "estado": "cancelada",
            "penalizacion": tardia,
        }