from piezas_y_casillas_const import BP, NP, BC, NC, BA, NA, BT, NT, BD, ND, BR, NR

MOVIMIENTOS_PEON_BLANCO = [
    (-1, 0), (-2, 0), (-1, 1), (-1, -1)
]

MOVIMIENTOS_PEON_NEGRO = [
    (1, 0), (2, 0), (1, 1), (1, -1)
]

MOVIMIENTOS_CABALLO = [
    (2,  1), (1,  2), (2, -1), (1, -2),
    (-2, -1), (-2,  1), (-1,  2), (-1, -2),
]

MOVIMIENTOS_ALFIL = [
    (1, 1), (1, -1), (-1, 1), (-1, -1)
]

MOVIMIENTOS_TORRE = [
    (1, 0), (0, 1), (-1, 0), (0, -1)
]

MOVIMIENTOS_REY = [
    (-1, 0), (-1, 1), (0, 1), (1, 1), 
    (1, 0), (1, -1), (0, -1), (-1, -1)
]

MOVIMIENTOS_REY_ATAQUE_BP = [
    (1, 1), (1, -1)
]

MOVIMIENTOS_REY_ATAQUE_NP = [
    (-1, 1), (-1, -1)
]

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
