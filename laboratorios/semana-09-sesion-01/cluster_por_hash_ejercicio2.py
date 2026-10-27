"""Ejercicio 2: sharding por hash del estudiante, consulta dirigida y
scatter-gather.

Corre las pruebas con:

    pytest test_cluster_por_hash_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""

from datos_reservas import hash_estable


class ClusterPorHash:
    def __init__(self, cantidad_de_shards):
        self.cantidad_de_shards = cantidad_de_shards
        self.shards = []
        for _ in range(cantidad_de_shards):
            self.shards.append([])

    def shard_de(self, id_estudiante):
        # TODO: devuelve el shard (0 a cantidad_de_shards - 1) de este
        # estudiante: el hash estable de su id, modulo la cantidad de
        # shards.
        return hash_estable(id_estudiante) % self.cantidad_de_shards

    def insertar(self, reserva):
        # TODO: agrega la reserva a la lista del shard que le corresponde
        # segun su id_estudiante.
        shard_id = self.shard_de(reserva.id_estudiante)
        self.shards[shard_id].append(reserva)

    def tamanos(self):
        # TODO: devuelve una lista con cuantas reservas tiene cada shard.
        contar = []

        for shard in self.shards:
            contar.append(len(shard))

        return contar

    def reservas_de_estudiante(self, id_estudiante):
        # TODO: consulta dirigida. Devuelve una tupla
        # (reservas_encontradas, shards_consultados), revisando solo el
        # shard donde viven las reservas de ese estudiante.
        reservas_estudiantes = []

        shard_id = self.shard_de(id_estudiante)

        for reserva in self.shards[shard_id]:
            if reserva.id_estudiante == id_estudiante:
                reservas_estudiantes.append(reserva)

        return reservas_estudiantes, 1

    def reservas_de_cancha(self, campus, cancha, fecha):
        # TODO: devuelve una tupla (reservas_encontradas,
        # shards_consultados) con todas las reservas de esa cancha, de ese
        # campus, en esa fecha. Piensa primero en cuantos shards tienes
        # que revisar para no perder ninguna.
        reservas_encontradas = []

        for shard in self.shards:
            for reserva in shard:
                if (
                    reserva.campus == campus
                    and reserva.cancha == cancha
                    and reserva.fecha == fecha
                ):
                    reservas_encontradas.append(reserva)

        return reservas_encontradas, self.cantidad_de_shards


def fraccion_que_cambia_de_shard(claves, shards_antes, shards_despues):
    # TODO: devuelve que fraccion de las claves (entre 0 y 1) cae en un
    # shard distinto al pasar de "shards_antes" a "shards_despues" shards
    # con este mismo reparto por hash y modulo.
    cambia = 0

    for clave in claves:
        if (
            hash_estable(clave) % shards_antes
            != hash_estable(clave) % shards_despues
        ):
            cambia += 1

    return cambia / len(claves)