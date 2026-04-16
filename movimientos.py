from piezas_y_casillas_const import *
from movimientos_const import *
from validaciones import *

def mov_peon(tablero, tablero_vacio, color, y, x, yv, xv):
    cfg = config_peon[color]
    dir = cfg['dir']
    
    if (yv == cfg['paso'] and y == yv + dir and x in [xv - 1, xv + 1] and tablero[yv][x] == cfg['rival_peon'] and
       estado_peones[cfg['rival_color']]['salto_doble'] and estado_peones[cfg['rival_color']]['columna'] == x):
        print(f"\n¡Captura al paso del peón {color}!")
        tablero[yv][x] = tablero_vacio[yv][x]
        return True

    # Movimiento normal (1 casilla)
    if y == yv + dir and x == xv and tablero[y][x] not in TOTAL_PIEZAS:
        return True
    
    # Movimiento doble (2 casillas)
    if yv == cfg['inicio'] and y == yv + 2*dir and x == xv and tablero[y+dir][x] not in TOTAL_PIEZAS and tablero[y][x] not in TOTAL_PIEZAS:
        estado_peones[color]['salto_doble'] = True
        estado_peones[color]['columna'] = x
        return True
    
    # Captura diagonal
    if y == yv + dir and x in [xv-1, xv+1] and tablero[y][x] in cfg['rivales']:
        return True
          
    return False
 
def mov_caballo(y, x, yv, xv):
    return any(y == yv + dy and x == xv + dx for dy, dx in MOVIMIENTOS_CABALLO)

def camino_libre(tablero, y, x, yv, xv):
    desplazamiento_x = (x > xv) - (x < xv)
    desplazamiento_y = (y > yv) - (y < yv)

    indice_x = xv + desplazamiento_x 
    indice_y = yv + desplazamiento_y
    
    while (indice_y, indice_x) != (y, x):
        if tablero[indice_y][indice_x] in TOTAL_PIEZAS:
            return False
        indice_x += desplazamiento_x
        indice_y += desplazamiento_y

    return True
    
def mov_alfil(tablero, y, x, yv, xv):
    if abs(x - xv) != abs(y - yv):
        return False

    return camino_libre(tablero, y, x, yv, xv)
 
def mov_torre(tablero, y, x, yv, xv):
    if xv != x and yv != y:
        return False
    
    es_movimiento_valido = camino_libre(tablero, y, x, yv, xv)
    
    if es_movimiento_valido:
        if (yv, xv) == (0, 0):
            estado_enroque['negro']['torre_izq_movida'] = True
        elif (yv, xv) == (0, 7):
            estado_enroque['negro']['torre_der_movida'] = True
        elif (yv, xv) == (7, 0):
            estado_enroque['blanco']['torre_izq_movida'] = True
        elif (yv, xv) == (7, 7):
            estado_enroque['blanco']['torre_der_movida'] = True 

    return es_movimiento_valido
 
def mov_reina(tablero, y, x, yv, xv):
    return mov_alfil(tablero, y, x, yv, xv) or mov_torre(tablero, y, x, yv, xv)

def mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco):
    color = "blanco" if es_turno_blanco else "negro"
    rey_actual = BR if es_turno_blanco else NR
    datos = estado_enroque[color]
    torre_aliada = datos['torre']
    rey_rival = datos['rey_rival']

    if abs(x - xv) <= 1 and abs(y - yv) <= 1: 
        if esta_amenazada(tablero, (y, x), rey_actual, es_turno_blanco):
            print(f"\n¡No puedes mover el rey {color} a esa posición porque estaría en jaque!")
            return False

        for dy, dx in MOVIMIENTOS_REY:
            yn, xn = y + dy, x + dx
            if validar_jaque(yn, xn, rey_rival):
                print(f"\n¡No puedes mover el rey {color} a esa posición porque chocaría con el rey rival!")
                return False

        datos['rey_movido'] = True
        return True            

    if es_jaque_actual or datos['rey_movido']:
        return False

    if x == xv + 2 and not datos['torre_der_movida'] and tablero[y][xv + 3] == torre_aliada:
        for dx in range(1, 3):
            if tablero[y][xv + dx] in TOTAL_PIEZAS_SR or esta_amenazada((y, xv + dx), rey_actual, es_turno_blanco):
                print("\n¡No puedes enrocar porque el rey pasaría por una casilla en jaque!, o hay una pieza obstaculo en el camino")
                return False
        
        print(f"\n¡Enroque corto rey {color}!")
        tablero[y][xv + 1] = torre_aliada
        tablero[y][xv + 3] = tablero_vacio[y][xv + 3]
        datos['rey_movido'] = True
        return True
    elif x == xv - 2 and not datos['torre_izq_movida'] and tablero[y][xv - 4] == torre_aliada:
        for dx in range(1, 4):
            if tablero[y][xv - dx] in TOTAL_PIEZAS_SR or esta_amenazada((y, xv - dx), rey_actual, es_turno_blanco):
                print("\n¡No puedes enrocar porque el rey pasaría por una casilla en jaque!, o hay una pieza obstaculo en el camino")
                return False
        
        print(f"\n¡Enroque largo rey {color}!")
        tablero[y][xv - 1] = torre_aliada
        tablero[y][xv - 4] = tablero_vacio[y][xv - 4]
        datos['rey_movido'] = True
        return True
    
    return False
    
def es_coordenada_valida(yn, xn):
    return 0 <= yn < 8 and 0 <= xn < 8

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
        if validar_jaque(yn, xn, peon_rival):
            atacantes.append(((yn, xn), peon_rival))

    for dy, dx in MOVIMIENTOS_CABALLO:
        yn, xn = ya + dy, xa + dx
        if validar_jaque(yn, xn, caballo_rival):
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
    pieza_enemigas_sr = piezas_negras_sr if es_turno_blanco else piezas_blancas_sr
    
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
            return not esta_amenazada((ye, xe), pieza_atacante, not es_turno_blanco)
        elif pieza_atacante in {BA, NA, BT, NT, BD, ND}:
            return es_mate_estrella(tablero, posicion_en_jaque, (ye, xe), pieza_atacante, es_turno_blanco)

    return False
