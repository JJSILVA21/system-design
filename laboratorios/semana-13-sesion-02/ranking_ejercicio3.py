"""Ejercicio 3: el orden del feed y los espacios mas reservados.

Mostrar el feed de lo mas nuevo a lo mas viejo es justo y es aburrido: un
entrenamiento de hace 5 minutos tapa el partido de tu propio equipo, que
ya tiene 40 confirmaciones. ReservaU pide un ranking simple, que se pueda
explicar en una oracion.

OrdenadorDeFeed se construye con dos diccionarios:
- interacciones: id de publicacion -> cuantas personas confirmaron
  asistencia o comentaron (0 si no aparece).
- equipos_de: estudiante -> lista de autores (equipos) en los que juega
  (lista vacia si no aparece).

Metodos:

- puntaje(publicacion, estudiante, ahora): (interacciones + 1) multiplicado
  por 3 si el autor es un equipo del estudiante (por 1 si no), dividido
  para (1 + horas), donde horas es (ahora - publicacion.momento) // 60
  (los momentos estan en minutos).

- ordenar(publicaciones, estudiante, ahora, cantidad): las `cantidad`
  publicaciones de mayor puntaje. En un empate de puntaje, primero la mas
  nueva (mayor momento), y si tambien empatan, la de id menor. Ademas,
  nunca tres seguidas del mismo autor: si la siguiente por puntaje seria
  la tercera seguida de ese autor, va la mejor de otro autor; si no queda
  ninguna de otro autor, va igual.

- espacios_mas_reservados(reservas, ahora, cantidad): reservas es una lista
  de tuplas (espacio, momento). Cuenta, por espacio, las reservas con
  momento en los ultimos 7 dias (ahora - 10080 < momento <= ahora), y
  devuelve una lista de tuplas (espacio, conteo) con los `cantidad` de
  mayor conteo; en un empate, primero el nombre menor. Los espacios sin
  reservas en esa ventana no aparecen.

Esta vez no hay codigo de partida. Corre las pruebas con:

    pytest test_ranking_ejercicio3.py
"""

from actividad import Publicacion


class OrdenadorDeFeed:
    def __init__(self, interacciones, equipos_de):
        self.interacciones = interacciones
        self.equipos_de = equipos_de

    def puntaje(self, publicacion, estudiante, ahora):
        cantidad_de_interacciones = self.interacciones.get(
            publicacion.id,
            0,
        )

        equipos = self.equipos_de.get(
            estudiante,
            [],
        )

        multiplicador = 1

        if publicacion.autor in equipos:
            multiplicador = 3

        horas = (
            ahora - publicacion.momento
        ) // 60

        return (
            (cantidad_de_interacciones + 1)
            * multiplicador
            / (1 + horas)
        )

    def ordenar(
        self,
        publicaciones,
        estudiante,
        ahora,
        cantidad,
    ):
        pendientes = sorted(
            publicaciones,
            key=lambda publicacion: (
                -self.puntaje(
                    publicacion,
                    estudiante,
                    ahora,
                ),
                -publicacion.momento,
                publicacion.id,
            ),
        )

        resultado = []

        while len(pendientes) > 0 and len(resultado) < cantidad:
            posicion = 0

            if len(resultado) >= 2:
                ultimo_autor = resultado[-1].autor
                penultimo_autor = resultado[-2].autor
                siguiente_autor = pendientes[0].autor

                if (
                    ultimo_autor == penultimo_autor
                    and siguiente_autor == ultimo_autor
                ):
                    for i in range(len(pendientes)):
                        if pendientes[i].autor != ultimo_autor:
                            posicion = i
                            break

            publicacion = pendientes.pop(posicion)
            resultado.append(publicacion)

        return resultado

    def espacios_mas_reservados(
        self,
        reservas,
        ahora,
        cantidad,
    ):
        conteos = {}
        inicio_de_la_ventana = ahora - 10080

        for espacio, momento in reservas:
            if inicio_de_la_ventana < momento <= ahora:
                conteos[espacio] = conteos.get(
                    espacio,
                    0,
                ) + 1

        ordenados = sorted(
            conteos.items(),
            key=lambda elemento: (
                -elemento[1],
                elemento[0],
            ),
        )

        return ordenados[:cantidad]