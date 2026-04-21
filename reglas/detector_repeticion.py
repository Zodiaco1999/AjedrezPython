historial_posiciones = {}

def serializar_tablero(tablero, es_turno_blanco):
    cadena = ""
    for fila in tablero:
        cadena += "".join(fila)
    cadena += f"_turno_{'blanco' if es_turno_blanco else 'negro'}"
    return cadena

def registrar_posicion(tablero, es_turno_blanco):
    posicion = serializar_tablero(tablero, es_turno_blanco)
    if posicion not in historial_posiciones:
        historial_posiciones[posicion] = 0
    historial_posiciones[posicion] += 1

def hay_repeticion_triple(tablero, es_turno_blanco):
    posicion = serializar_tablero(tablero, es_turno_blanco)
    return historial_posiciones.get(posicion, 0) >= 3