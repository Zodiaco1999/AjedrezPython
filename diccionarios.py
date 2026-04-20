from piezas_y_casillas_const import *

columnas_a_indices = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}
filas_a_indices = {
    '1': 7,
    '2': 6,
    '3': 5,
    '4': 4,
    '5': 3,
    '6': 2,
    '7': 1,
    '8': 0
} 

MENSAJES_ERROR = {
    "posicion_fuera": "¡La posición ingresada está fuera del tablero!",
    "casilla_vacia": "¡No ha seleccionado ninguna pieza!",
    "turno_incorrecto": "¡Esa pieza no pertenece a tu color!",
    "movimiento_ilegal": "¡Esa pieza no puede moverse así!",
    "rey_en_jaque": "¡Movimiento ilegal! Tu rey estaria en jaque.",
    "posicion_invalida": "¡Posición invalida!"
}

estado_enroque = {
    'blanco': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': BT, 
        'rey_rival': NR
    },
    'negro': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': NT, 
        'rey_rival': BR
    }
}

config_peon = {
    'blanco': {'dir': -1, 'inicio': 6, 'paso': 3, 'rival_peon': NP, 'rivales': piezas_negras_sr, 'rival_color': 'negro', 'coronacion': 0},
    'negro': {'dir': 1, 'inicio': 1, 'paso': 4, 'rival_peon': BP, 'rivales': piezas_blancas_sr, 'rival_color': 'blanco', 'coronacion': 7}
}

estado_peones = {
    'blanco': {'salto_doble': False , 'columna': None},
    'negro': {'salto_doble': False, 'columna': None}
}