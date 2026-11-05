"""Ejercicio 2: invalidar el cache al reservar, y darle a cada entrada un
tiempo de vida (TTL).

Corre las pruebas con:

    pytest test_invalidacion_ttl_ejercicio2.py

No cambies los nombres de la clase ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class ServicioConInvalidacionYTTL:
    def __init__(self, repositorio, reloj, ttl):
        self.repositorio = repositorio
        self.reloj = reloj
        self.ttl = ttl
        self.cache = {}
        self.aciertos = 0
        self.fallos = 0

    def disponibilidad(self, cancha, fecha):
        # TODO: cache-aside como en el Ejercicio 1, con dos cambios:
        # - Cada entrada de self.cache guarda una tupla
        #   (libres, instante_en_que_se_guardo), con el instante tomado de
        #   self.reloj.ahora().
        # - Una entrada solo cuenta como acierto si tiene menos de
        #   self.ttl segundos. Si ya vencio, es un fallo: consulta el
        #   repositorio y reemplaza la entrada.
        clave = (cancha, fecha)
        ahora = self.reloj.ahora()

        if clave in self.cache:
            libres, instante_guardado = self.cache[clave]
            edad = ahora - instante_guardado

            if edad < self.ttl:
                self.aciertos += 1
                return libres

        self.fallos += 1
        libres = self.repositorio.consultar_disponibilidad(
            cancha,
            fecha,
        )

        self.cache[clave] = (libres, ahora)
        return libres

    def reservar(self, cancha, fecha, hora):
        # TODO: verifica la disponibilidad directamente en el repositorio
        # (nunca en el cache: esta respuesta decide una escritura). Si la
        # hora no esta libre, devuelve False. Si esta libre, registra la
        # reserva en el repositorio, invalida la entrada (cancha, fecha)
        # del cache, aunque no exista, y devuelve True.
        libres = self.repositorio.consultar_disponibilidad(
            cancha,
            fecha,
        )

        if hora not in libres:
            return False

        self.repositorio.registrar_reserva(
            cancha,
            fecha,
            hora,
        )

        clave = (cancha, fecha)
        self.cache.pop(clave, None)

        return True