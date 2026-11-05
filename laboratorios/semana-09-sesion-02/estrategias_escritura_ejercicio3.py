"""Ejercicio 3: dos estrategias de escritura, write-through para las
reservas y write-back para el contador de visitas.

Corre las pruebas con:

    pytest test_estrategias_escritura_ejercicio3.py

No cambies los nombres de las clases ni de los metodos: los tests
dependen de que existan exactamente asi.
"""


class DisponibilidadWriteThrough:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.cache = {}

    def disponibilidad(self, cancha, fecha):
        # TODO: igual que cache-aside: si (cancha, fecha) no esta en
        # self.cache, consulta el repositorio y guarda la respuesta.
        # Devuelve lo que quede guardado.
        clave = (cancha, fecha)

        if clave not in self.cache:
            libres = self.repositorio.consultar_disponibilidad(
                cancha,
                fecha,
            )
            self.cache[clave] = libres

        return self.cache[clave]

    def reservar(self, cancha, fecha, hora):
        # TODO: write-through. Verifica la hora en el repositorio y, si no
        # esta libre, devuelve False. Si esta libre, escribe la reserva en
        # el repositorio y, en la misma operacion, actualiza la entrada
        # del cache (si existe) para que ya no muestre esa hora como
        # libre, en vez de borrarla. Devuelve True.
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

        if clave in self.cache and hora in self.cache[clave]:
            self.cache[clave].remove(hora)

        return True


class VisitasWriteBack:
    def __init__(self, repositorio):
        self.repositorio = repositorio
        self.pendientes = {}

    def registrar_visita(self, cancha):
        # TODO: write-back. Suma 1 a la cuenta de esa cancha en
        # self.pendientes, sin escribir nada en el repositorio.
        self.pendientes[cancha] = self.pendientes.get(cancha, 0) + 1

    def visitas(self, cancha):
        # TODO: devuelve el total de visitas de la cancha: lo que ya esta
        # en el repositorio mas lo que todavia esta pendiente en el cache.
        guardadas = self.repositorio.visitas_de(cancha)
        pendientes = self.pendientes.get(cancha, 0)

        return guardadas + pendientes

    def vaciar(self):
        # TODO: escribe en el repositorio, con una sola llamada a
        # sumar_visitas(...) por cancha, todas las visitas pendientes, y
        # deja self.pendientes vacio.
        for cancha, cantidad in self.pendientes.items():
            self.repositorio.sumar_visitas(cancha, cantidad)

        self.pendientes = {}

    def caer(self):
        # Simula que el proceso del cache se reinicia: lo que no se vacio
        # al repositorio se pierde. Ya esta completo.
        self.pendientes = {}