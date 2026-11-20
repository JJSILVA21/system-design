"""Ejercicio 3: reconectarse sin perder avisos.

Un telefono que pasa por un tunel pierde la conexion durante un minuto.
Cuando vuelve, abre una conexion nueva, pero los avisos que se publicaron
mientras tanto ya no le llegan: su calendario queda desactualizado sin
que nadie lo note. ReservaU pide esto:

CanalConHistorial es un intermediario como Canales (puedes heredar de el,
en canales_ejercicio1.py) que numera los mensajes de cada tema y guarda
los ultimos. Se construye con CanalConHistorial(historial=50).

- publicar(tema, mensaje): el primer mensaje de cada tema es el numero 1,
  el siguiente el 2, y asi. A cada conexion suscrita le envia el numero,
  un espacio y el mensaje: "3 ocupada 18-19". Guarda ese texto con su
  numero en el historial del tema, que conserva solo los ultimos
  `historial` mensajes (los mas viejos se descartan). Devuelve el numero.
- ultimo_numero(tema): el numero del ultimo mensaje publicado en el tema,
  o 0 si no hay ninguno.
- reconectar(tema, conexion, ultimo_visto): la app dice cual fue el
  ultimo numero que alcanzo a recibir.
  - Si ultimo_visto es mayor que ultimo_numero(tema): ValueError("numero
    desconocido"), sin suscribir.
  - Si alguno de los mensajes que se perdio ya no esta en el historial,
    le envia un solo mensaje, "recargar" (la app tiene que pedir el
    calendario completo).
  - Si no, le envia, en orden, los mensajes del historial con numero
    mayor que ultimo_visto, con el mismo texto que se envio la primera
    vez.
  - En los dos ultimos casos, despues la suscribe al tema.
- suscribir, desuscribir y suscriptores, como en Canales.

Esta vez no hay codigo de partida. Corre las pruebas con:

    pytest test_reconexion_ejercicio3.py
"""

from canales_ejercicio1 import Canales


class CanalConHistorial(Canales):
    def __init__(self, historial=50):
        super().__init__()
        self.cantidad_de_historial = historial
        self.numeros = {}
        self.historiales = {}

    def publicar(self, tema, mensaje):
        numero = self.ultimo_numero(tema) + 1
        self.numeros[tema] = numero

        texto = str(numero) + " " + mensaje

        if tema not in self.historiales:
            self.historiales[tema] = []

        self.historiales[tema].append(
            (numero, texto)
        )

        if len(self.historiales[tema]) > self.cantidad_de_historial:
            self.historiales[tema].pop(0)

        super().publicar(
            tema,
            texto,
        )

        return numero

    def ultimo_numero(self, tema):
        return self.numeros.get(tema, 0)

    def reconectar(self, tema, conexion, ultimo_visto):
        ultimo_publicado = self.ultimo_numero(tema)

        if ultimo_visto > ultimo_publicado:
            raise ValueError("numero desconocido")

        historial = self.historiales.get(tema, [])

        if ultimo_visto < ultimo_publicado:
            if len(historial) == 0:
                conexion.enviar("recargar")
            else:
                primer_numero_guardado = historial[0][0]
                siguiente_necesario = ultimo_visto + 1

                if siguiente_necesario < primer_numero_guardado:
                    conexion.enviar("recargar")
                else:
                    for numero, texto in historial:
                        if numero > ultimo_visto:
                            conexion.enviar(texto)

        self.suscribir(
            tema,
            conexion,
        )