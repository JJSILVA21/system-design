"""Ejercicio 3: balanceador de menos conexiones (least connections).

Corre las pruebas con:

    pytest test_menos_conexiones_ejercicio3.py

Las pruebas tambien usan tu BalanceadorRoundRobin del Ejercicio 2, para
comparar los dos algoritmos con el mismo trafico.
"""


class BalanceadorMenosConexiones:
    def __init__(self, servidores):
        self.servidores = servidores

    def enviar(self, duracion):
        elegido = None
        for servidor in self.servidores:
            if servidor.health_check() and servidor.puede_atender():
                if (elegido is None or servidor.conexiones_activas() < elegido.conexiones_activas()):
                    elegido = servidor
            if elegido is None:
                return None
        elegido.atender(duracion)
        return elegido.nombre

    # TODO: elige, entre los servidores sanos que todavia pueden
            # atender, el que tiene menos conexiones activas en este momento.
            # Si hay empate, gana el que aparece primero en la lista.
            # Enviale la solicitud y devuelve su nombre. Si ningun servidor
            # puede atenderla, devuelve None.
