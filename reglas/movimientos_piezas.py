from constantes.piezas import (TOTAL_PIEZAS, TOTAL_PIEZAS_SR, PIEZAS_BLANCAS, PIEZAS_NEGRAS, 
 BP, NP, BC, NC, BA, NA, BT, NT, BD, ND, BR, NR)
from constantes.movimientos import MOVIMIENTOS_CABALLO
from estado.estados_piezas import estado_enroque, estado_peones, config_peon
from presentacion.mensajes import mensaje_pieza
from reglas.detector_jaque import esta_amenazada

def movimiento_pieza(tablero, tablero_vacio, p, x, y, xv, yv, es_jaque_actual, es_turno_blanco, es_simulacion=False):
    global pieza_selec
    color = "blanco" if es_turno_blanco else "negro"
    
    if x == xv and y == yv:
        print("\n¡No puedes mover la pieza a su propia posición!")
        return False
    
    if not ((p in PIEZAS_BLANCAS and tablero[y][x] not in PIEZAS_BLANCAS + NR) or 
            (p in PIEZAS_NEGRAS and tablero[y][x] not in PIEZAS_NEGRAS + BR)):
        return False

    movimientos_piezas = {
        BP: lambda: mov_peon(tablero, tablero_vacio, color, y, x, yv, xv, es_simulacion),
        NP: lambda: mov_peon(tablero, tablero_vacio, color, y, x, yv, xv, es_simulacion),
        BC: lambda: mov_caballo(y, x, yv, xv),
        NC: lambda: mov_caballo(y, x, yv, xv),
        BA: lambda: mov_alfil(tablero, y, x, yv, xv),
        NA: lambda: mov_alfil(tablero, y, x, yv, xv),        
        BT: lambda: mov_torre(tablero, y, x, yv, xv),
        NT: lambda: mov_torre(tablero, y, x, yv, xv),
        BD: lambda: mov_reina(tablero, y, x, yv, xv),
        ND: lambda: mov_reina(tablero, y, x, yv, xv),
        BR: lambda: mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco, es_simulacion),
        NR: lambda: mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco, es_simulacion),
    }

    return movimientos_piezas[p]()

def mov_peon(tablero, tablero_vacio, color, y, x, yv, xv, es_simulacion):
    cfg = config_peon[color]
    dir = cfg['dir']
    
    if (yv == cfg['paso'] and y == yv + dir and x in [xv - 1, xv + 1] and tablero[yv][x] == cfg['rival_peon'] and
       estado_peones[cfg['rival_color']]['salto_doble'] and estado_peones[cfg['rival_color']]['columna'] == x):
        mensaje_pieza(es_simulacion, f"¡Captura al paso del peón {color}!")
        tablero[yv][x] = tablero_vacio[yv][x]
        return True

    # Movimiento normal (1 casilla)
    if y == yv + dir and x == xv and tablero[y][x] not in TOTAL_PIEZAS:
        return True
    
    # Movimiento doble (2 casillas)
    if yv == cfg['inicio'] and y == yv + 2*dir and x == xv and tablero[yv+dir][x] not in TOTAL_PIEZAS and tablero[y][x] not in TOTAL_PIEZAS:
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

def mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco, es_simulacion):
    color = "blanco" if es_turno_blanco else "negro"
    rey_actual = BR if es_turno_blanco else NR
    datos = estado_enroque[color]
    torre_aliada = datos['torre']
    rey_rival = datos['rey_rival']

    if abs(x - xv) <= 1 and abs(y - yv) <= 1: 
        if esta_amenazada(tablero, (y, x), rey_actual, es_turno_blanco):
            mensaje_pieza(es_simulacion, f"¡No puedes mover el rey {color} a esa posición porque estaría en jaque!")
            return False

        datos['rey_movido'] = True
        return True            

    if es_jaque_actual or datos['rey_movido']:
        return False

    if x == xv + 2 and not datos['torre_der_movida'] and tablero[y][xv + 3] == torre_aliada:
        for dx in range(1, 3):
            if tablero[y][xv + dx] in TOTAL_PIEZAS_SR or esta_amenazada(tablero, (y, xv + dx), rey_actual, es_turno_blanco):
                mensaje_pieza(es_simulacion, "¡No puedes enrocar porque el rey pasaría por una casilla en jaque!, o hay una pieza obstaculo en el camino")
                return False
        
        print(f"\n¡Enroque corto rey {color}!")
        tablero[y][xv + 1] = torre_aliada
        tablero[y][xv + 3] = tablero_vacio[y][xv + 3]
        datos['rey_movido'] = True
        return True
    elif x == xv - 2 and not datos['torre_izq_movida'] and tablero[y][xv - 4] == torre_aliada:
        for dx in range(1, 4):
            if tablero[y][xv - dx] in TOTAL_PIEZAS_SR or esta_amenazada(tablero, (y, xv - dx), rey_actual, es_turno_blanco):
                mensaje_pieza(es_simulacion, "¡No puedes enrocar porque el rey pasaría por una casilla en jaque!, o hay una pieza obstaculo en el camino")
                return False
        
        print(f"\n¡Enroque largo rey {color}!")
        tablero[y][xv - 1] = torre_aliada
        tablero[y][xv - 4] = tablero_vacio[y][xv - 4]
        datos['rey_movido'] = True
        return True
    
    return False
