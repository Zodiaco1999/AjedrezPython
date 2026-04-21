from constantes.piezas import (
    BP, NP, BC, NC, BA, NA, BT, NT, BD, ND,
    CASILLAS_VACIAS, PIEZAS_BLANCAS_SR, PIEZAS_NEGRAS_SR
)
from constantes.movimientos import (
    MOVIMIENTOS_CABALLO, MOVIMIENTOS_ALFIL, MOVIMIENTOS_TORRE, MOVIMIENTOS_REY,
    MOVIMIENTOS_REY_ATAQUE_BP, MOVIMIENTOS_REY_ATAQUE_NP
)
from utilidades.validaciones_basicas import es_coordenada_valida

def validar_jaque(tablero, yn, xn, pieza_objetivo):
    return es_coordenada_valida(yn, xn) and tablero[yn][xn] == pieza_objetivo

def buscar_atacantes_estrella(tablero, posicion_amenazada, pieza_actual, movimientos, set_piezas_rivales):
    ya, xa = posicion_amenazada
    atacantes_encontrados = []
    for dy, dx in movimientos:
        yn, xn = ya + dy, xa + dx
        while es_coordenada_valida(yn, xn):
            posicion_nueva = tablero[yn][xn]
            if posicion_nueva not in CASILLAS_VACIAS | {pieza_actual}:
                if posicion_nueva in set_piezas_rivales:
                    atacantes_encontrados.append(((yn, xn), posicion_nueva))
                break
            yn += dy
            xn += dx
            
    return atacantes_encontrados

def obtener_atacantes(tablero, posicion_amenazada, pieza_actual, es_turno_blanco):
    ya, xa = posicion_amenazada
    atacantes = []
    
    peon_rival = NP if es_turno_blanco else BP
    caballo_rival = NC if es_turno_blanco else BC
    alfil_rival = NA if es_turno_blanco else BA
    torre_rival = NT if es_turno_blanco else BT
    dama_rival = ND if es_turno_blanco else BD
    movimientos_peon_rival = MOVIMIENTOS_REY_ATAQUE_NP if es_turno_blanco else MOVIMIENTOS_REY_ATAQUE_BP

    for dy, dx in movimientos_peon_rival:
        yn, xn = ya + dy, xa + dx
        if validar_jaque(tablero, yn, xn, peon_rival):
            atacantes.append(((yn, xn), peon_rival))

    for dy, dx in MOVIMIENTOS_CABALLO:
        yn, xn = ya + dy, xa + dx
        if validar_jaque(tablero, yn, xn, caballo_rival):
            atacantes.append(((yn, xn), caballo_rival))

    atacantes_diagonales = {alfil_rival, dama_rival}
    atacantes.extend(
        buscar_atacantes_estrella(tablero, (ya, xa), pieza_actual, MOVIMIENTOS_ALFIL, atacantes_diagonales)
    )

    atacantes_ortogonales = {torre_rival, dama_rival}
    atacantes.extend(
        buscar_atacantes_estrella(tablero, (ya, xa), pieza_actual, MOVIMIENTOS_TORRE, atacantes_ortogonales)
    )

    return atacantes

def esta_amenazada(tablero, posicion_pieza, pieza_actual, es_turno_blanco):
    return len(obtener_atacantes(tablero, posicion_pieza, pieza_actual, es_turno_blanco)) > 0

def detalles_jaque(tablero, posicion_rey, pieza_actual, es_turno_blanco):
    return obtener_atacantes(tablero, posicion_rey, pieza_actual, es_turno_blanco)

def es_mate_estrella(tablero, posicion_rey, atacante_jaque, pieza_atacante, es_turno_blanco):
    rey_y, rey_x = posicion_rey
    ye, xe = atacante_jaque
    paso_y = paso_x = 0
    
    if abs(xe - rey_x) == abs(ye - rey_y):
        paso_y = 1 if rey_y > ye else -1
        paso_x = 1 if rey_x > xe else -1
    elif xe == rey_x or ye == rey_y:
        paso_y = (rey_y > ye) - (rey_y < ye)
        paso_x = (rey_x > xe) - (rey_x < xe)
            
    y = ye
    x = xe  
    while (y, x) != (rey_y, rey_x):
        if esta_amenazada(tablero, (y, x), pieza_atacante, not es_turno_blanco):
            return False
        y += paso_y
        x += paso_x
    
    return True

def es_jaque_mate(tablero, posicion_en_jaque, es_turno_blanco, atacantes_jaque):
    rey_y, rey_x = posicion_en_jaque
    pieza_actual = tablero[rey_y][rey_x]
    casillas_en_jaque = 0
    pieza_enemigas_sr = PIEZAS_NEGRAS_SR if es_turno_blanco else PIEZAS_BLANCAS_SR
    
    for dy, dx in MOVIMIENTOS_REY:
        yn, xn = rey_y + dy, rey_x + dx
        if not es_coordenada_valida(yn, xn) or tablero[yn][xn] not in CASILLAS_VACIAS:
            casillas_en_jaque += 1
        elif (tablero[yn][xn] in CASILLAS_VACIAS or tablero[yn][xn] in pieza_enemigas_sr) and esta_amenazada(tablero, (yn, xn), pieza_actual, es_turno_blanco):
            casillas_en_jaque += 1
    
    rey_sin_movimientos = casillas_en_jaque == len(MOVIMIENTOS_REY)
            
    if rey_sin_movimientos:
        ye, xe = atacantes_jaque[0][0]
        pieza_atacante = atacantes_jaque[0][1]
        

        if pieza_atacante in {BP, NP, BC, NC}:
            return not esta_amenazada(tablero, (ye, xe), pieza_atacante, not es_turno_blanco)
        elif pieza_atacante in {BA, NA, BT, NT, BD, ND}:
            return es_mate_estrella(tablero, posicion_en_jaque, (ye, xe), pieza_atacante, es_turno_blanco)

    return False
