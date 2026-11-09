"""Los casos de uso de ReservaU: lo que la aplicacion hace, paso a paso.
Solo conoce el dominio y los puertos.
"""

from dominio import motivo_de_rechazo


class ReservarCancha:
    def __init__(self, repositorio):
        self.repositorio = repositorio

    def ejecutar(self, estudiante, cancha, fecha, hora):
        # TODO 2: pregunta al repositorio si la hora esta ocupada y cuantas
        # reservas tiene el estudiante ese dia, y decide con
        # motivo_de_rechazo. Si hay motivo, devuelve
        # {"estado": "rechazada", "motivo": motivo}. Si no, guarda y
        # devuelve {"estado": "confirmada", "reserva": la Reserva guardada}.
        hora_ocupada = self.repositorio.ocupada(
            cancha,
            fecha,
            hora,
        )

        reservas_del_dia = self.repositorio.contar_del_estudiante(
            estudiante,
            fecha,
        )

        motivo = motivo_de_rechazo(
            cancha,
            hora,
            hora_ocupada,
            reservas_del_dia,
        )

        if motivo is not None:
            return {
                "estado": "rechazada",
                "motivo": motivo,
            }

        reserva = self.repositorio.guardar(
            estudiante,
            cancha,
            fecha,
            hora,
        )

        return {
            "estado": "confirmada",
            "reserva": reserva,
        }