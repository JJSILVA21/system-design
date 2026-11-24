"""Ejercicio 1: las penalizaciones por cancelar tarde, con TDD.

Este archivo empieza vacio a proposito: el codigo se escribe solo para
hacer pasar una prueba que fallo. La regla de ReservaU:

- Cancelar con 24 horas (1440 minutos) o mas de anticipacion: 0 puntos.
- Cancelar con menos de 24 horas y 2 horas (120 minutos) o mas: 1 punto.
- Cancelar con menos de 2 horas: 2 puntos.
- No presentarse (la reserva paso sin cancelar): 3 puntos.
- Un estudiante con 3 puntos o mas en el semestre queda bloqueado: no
  puede reservar hasta que el semestre termine.

Lista de pruebas, en el orden en que se escriben (se pueden agregar mas):

1. Cancelar con 2000 minutos de anticipacion da 0 puntos.
2. Cancelar con 600 minutos da 1 punto.
3. Cancelar con 30 minutos da 2 puntos.
4. Los bordes: 1440 minutos da 0, 120 da 1.
5. No presentarse da 3 puntos.
6. Un estudiante sin penalizaciones no esta bloqueado.
7. Con 1 punto y despues 2, queda bloqueado.
8. Las penalizaciones de un estudiante no bloquean a otro.

Corre las pruebas con:

    pytest test_penalizaciones_ejercicio1.py
"""

PUNTOS_PARA_BLOQUEAR = 3

def puntos_por_cancelar(minutos: int):
    if minutos >= 1440:
        return 0
    elif minutos >= 120 and minutos < 1440:
        return 1
    elif minutos >= 0 and minutos < 120:
        return 2
    else:
        return 3
    
class HistoriaDePenalizaciones: 
    def __init__(self):
        self._puntos = {}

    def esta_bloqueado(self, estudiante):
        if estudiante not in self._puntos:
            self._puntos[estudiante] = 0
        return self._puntos[estudiante] >= PUNTOS_PARA_BLOQUEAR

    def _sumar(self, estudiante, puntos):
        if estudiante not in self._puntos:
            self._puntos[estudiante] = 0
        self._puntos[estudiante] += puntos
        
    def cancelar(self, estudiante, minutos):
        self._sumar(estudiante, puntos_por_cancelar(minutos))

    
        
