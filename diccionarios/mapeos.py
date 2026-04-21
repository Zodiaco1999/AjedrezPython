from constantes.piezas import BP, BC, BA, BT, BR, BD, NP, NC, NA, NT, NR, ND
from constantes.movimientos import (
    MOVIMIENTOS_PEON_BLANCO, MOVIMIENTOS_PEON_NEGRO, MOVIMIENTOS_CABALLO,
    MOVIMIENTOS_ALFIL, MOVIMIENTOS_TORRE, MOVIMIENTOS_REY
)

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

MOVIMIENTOS_POR_PIEZA = {
    BP: MOVIMIENTOS_PEON_BLANCO,
    NP: MOVIMIENTOS_PEON_NEGRO,
    BC: MOVIMIENTOS_CABALLO,
    NC: MOVIMIENTOS_CABALLO,
    BA: MOVIMIENTOS_ALFIL,
    NA: MOVIMIENTOS_ALFIL,
    BT: MOVIMIENTOS_TORRE,
    NT: MOVIMIENTOS_TORRE,
    BD: MOVIMIENTOS_TORRE + MOVIMIENTOS_ALFIL,
    ND: MOVIMIENTOS_TORRE + MOVIMIENTOS_ALFIL,
    BR: MOVIMIENTOS_REY,
    NR: MOVIMIENTOS_REY,
}