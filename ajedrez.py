from piezas_y_casillas import *
from movimientos import *
from validaciones import *
import copy

fila_p = []
fila_i = []
tablero = []
tablero_vacio = []
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
x = 0
y = 0
turno = 1
pieza_selec = ""

# LLenar los tableros con las casillas negras y blancas
for t in range(4):
    for i in range(8):
        if i % 2 == 0:
            fila_p.append(B)
        else:
            fila_p.append(N)

        fila_i.insert(0, fila_p[i])

    tablero.append(fila_p[:8])
    tablero.append(fila_i[:8]) 
    tablero_vacio.append(fila_p[:8])
    tablero_vacio.append(fila_i[:8])

def nomenclatura_columnas():
    print("    A     B     C     D     E     F     G     H")   
       
# Imprimir el tablero en orden 
def imprimir_tablero():
    print()
    nomenclatura_columnas()
    for i in range(8):
        print(8 - i,tablero[i][:],8 - i)
    nomenclatura_columnas()

# Asignando las piezas blancas
tablero[6] = [BP] * 8
tablero[7][1] = tablero[7][6] = BC
tablero[7][2] = tablero[7][5] = BA
tablero[7][0] = tablero[7][7] = BT
tablero[2][7] = BD
tablero[7][4] = BR
# Asignando las piezas negras
#tablero[1] = [NP] * 8
# tablero[0][1] = tablero[0][6] = NC
# tablero[0][2] = tablero[0][5] = NA
# tablero[0][0] = tablero[0][7] = NT
# tablero[0][7] = ND
tablero[1][1] = NR

def turnos(t):
    es_turno_blanco = t % 2 != 0
    color = "blanco" if es_turno_blanco else "negro"
    estado_peones[color]['salto_doble'] = False
    estado_peones[color]['columna'] = None
    
    print(f"\n================Turno de las {'blancas' if es_turno_blanco else 'negras'}================")
    return es_turno_blanco

def es_posicion_valida(p):
    if len(p) != 2:
        return False
    
    global x, y
 
    p = p.lower() 
    
    x = columnas_a_indices.get(p[0])
    y = filas_a_indices.get(p[1])
    
    if x is None or y is None:
        return False
    
    return True
            
def es_movimiento_valido(yn, xn):
    return 0 <= yn < 8 and 0 <= xn < 8

def es_pieza_actual(pieza):
    return pieza_selec == pieza
            
def coronar_peon(color, es_coronacion):
    if not es_coronacion:
        return None
    
    piezas_coronacion = f"d){BD}, t){BT}, a){BA}, c){BC}" if color == "blanco" else f"d){ND}, t){NT}, a){NA}, c){NC}"
    print("\n¡Tu peón ha llegado al final del tablero!")
    
    selec_pieza_coronada = None
    while selec_pieza_coronada not in ['c', 'a', 't', 'd']:
        selec_pieza_coronada = input(f"Ingresa la pieza que deseas coronar\n{piezas_coronacion} ").lower()
    
    mapeo_piezas = {
        'c': BC if color == "blanco" else NC,
        'a': BA if color == "blanco" else NA,
        't': BT if color == "blanco" else NT,
        'd': BD if color == "blanco" else ND
    }
    
    return mapeo_piezas[selec_pieza_coronada]

def mov_peon(color, y, x, yv, xv):
    cfg = config_peon[color]
    dir = cfg['dir']
    
    if (yv == cfg['paso'] and y == yv + dir and x in [xv - 1, xv + 1] and tablero[yv][x] == cfg['rival_peon'] and
       estado_peones[cfg['rival_color']]['salto_doble'] and estado_peones[cfg['rival_color']]['columna'] == x):
        print(f"\n¡Captura al paso del peón {color}!")
        tablero[yv][x] = tablero_vacio[yv][x]
        return True, None

    # Movimiento normal (1 casilla)
    if y == yv + dir and x == xv and tablero[y][x] not in TOTAL_PIEZAS:
        pieza_coronada = coronar_peon(color, y == cfg['coronacion'])
        return True, pieza_coronada
    
    # Movimiento doble (2 casillas)
    if yv == cfg['inicio'] and y == yv + 2*dir and x == xv and tablero[y+dir][x] not in TOTAL_PIEZAS and tablero[y][x] not in TOTAL_PIEZAS:
        estado_peones[color]['salto_doble'] = True
        estado_peones[color]['columna'] = x
        return True, None
    
    # Captura diagonal
    if y == yv + dir and x in [xv-1, xv+1] and tablero[y][x] in cfg['rivales']:
        pieza_coronada = coronar_peon(color, y == cfg['coronacion'])
        return True, pieza_coronada
          
    return False, None
 
def mov_caballo():
    if ((xv + 2 == x or xv - 2 == x) and (yv - 1 == y or yv + 1 == y)) or ((xv + 1 == x or xv - 1 == x) and (yv - 2 == y or yv + 2 == y)):
        return True

def camino_libre():
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
    
def mov_alfil():
    if abs(x - xv) != abs(y - yv):
        return False

    return camino_libre()
 
def mov_torre():
    if xv != x and yv != y:
        return False
    
    es_movimiento_valido = camino_libre()
    
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
 
def mov_reina():
    return mov_alfil() or mov_torre()

def mov_rey(y, x, yv, xv, es_jaque_actual, es_turno_blanco):
    color = "blanco" if es_turno_blanco else "negro"
    rey_actual = BR if es_turno_blanco else NR
    datos = estado_enroque[color]
    torre_aliada = datos['torre']
    rey_rival = datos['rey_rival']

    if abs(x - xv) <= 1 and abs(y - yv) <= 1: 
        if esta_amenazada((y, x), rey_actual, es_turno_blanco):
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
    
def hallar_posicion_pieza(tablero, pieza_buscada):
    for y, fila in enumerate(tablero):
        if pieza_buscada in fila:
            x = fila.index(pieza_buscada)
            return [y, x]
    return None

def validar_jaque(yn, xn, pieza_objetivo):
    return es_movimiento_valido(yn, xn) and tablero[yn][xn] == pieza_objetivo

def obtener_atacantes(posicion_amenazada, pieza_actual, es_turno_blanco):
    ya, xa = posicion_amenazada
    atacantes = []
    
    peon_rival = NP if es_turno_blanco else BP
    caballo_rival = NC if es_turno_blanco else BC
    alfil_rival = NA if es_turno_blanco else BA
    torre_rival = NT if es_turno_blanco else BT
    dama_rival = ND if es_turno_blanco else BD
    movimientos_peon_rival = MOVIMIENTOS_PEON_NEGRO if es_turno_blanco else MOVIMIENTOS_PEON_BLANCO

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
        buscar_atacantes_estrella((ya, xa), pieza_actual, MOVIMIENTOS_ALFIL, atacantes_diagonales)
    )

    atacantes_ortogonales = {torre_rival, dama_rival}
    atacantes.extend(
        buscar_atacantes_estrella((ya, xa), pieza_actual, MOVIMIENTOS_TORRE, atacantes_ortogonales)
    )

    return atacantes

def buscar_atacantes_estrella(posicion_amenazada, pieza_actual, movimientos, set_piezas_rivales):
    ya, xa = posicion_amenazada
    atacantes_encontrados = []
    for dy, dx in movimientos:
        yn, xn = ya + dy, xa + dx
        while es_movimiento_valido(yn, xn):
            posicion_nueva = tablero[yn][xn]
            if posicion_nueva not in CASILLAS_VACIAS | {pieza_actual}:
                if posicion_nueva in set_piezas_rivales:
                    atacantes_encontrados.append(((yn, xn), posicion_nueva))
                break
            yn += dy
            xn += dx
            
    return atacantes_encontrados

def esta_amenazada(posicion_pieza, pieza_actual, es_turno_blanco):
    return len(obtener_atacantes(posicion_pieza, pieza_actual, es_turno_blanco)) > 0

def detalles_jaque(posicion_rey, pieza_actual, es_turno_blanco):
    return obtener_atacantes(posicion_rey, pieza_actual, es_turno_blanco)

def es_mate_estrella(posicion_rey, atacante_jaque, pieza_atacante, es_turno_blanco):
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
        if esta_amenazada((y, x), pieza_atacante, not es_turno_blanco):
            return False
        y += paso_y
        x += paso_x
    
    return True

def es_jaque_mate(posicion_en_jaque, es_turno_blanco, atacantes_jaque):
    rey_y, rey_x = posicion_en_jaque
    pieza_actual = tablero[rey_y][rey_x]
    casillas_en_jaque = 0
    pieza_enemigas_sr = piezas_negras_sr if es_turno_blanco else piezas_blancas_sr
    
    for dy, dx in MOVIMIENTOS_REY:
        yn, xn = rey_y + dy, rey_x + dx
        if not es_movimiento_valido(yn, xn) or tablero[yn][xn] not in CASILLAS_VACIAS:
            casillas_en_jaque += 1
        elif (tablero[yn][xn] in CASILLAS_VACIAS or tablero[yn][xn] in pieza_enemigas_sr) and esta_amenazada((yn, xn), pieza_actual, es_turno_blanco):
            casillas_en_jaque += 1
    
    rey_sin_movimientos = casillas_en_jaque == len(MOVIMIENTOS_REY)
            
    if rey_sin_movimientos:
        ye, xe = atacantes_jaque[0][0]
        pieza_atacante = atacantes_jaque[0][1]
        

        if pieza_atacante in {BP, NP, BC, NC}:
            return not esta_amenazada((ye, xe), pieza_atacante, not es_turno_blanco)
        elif pieza_atacante in {BA, NA, BT, NT, BD, ND}:
            return es_mate_estrella(posicion_en_jaque, (ye, xe), pieza_atacante, es_turno_blanco)

    return False

def reiniciar_turno():
    global turno
    global x
    global y
    x = xv
    y = yv
    turno -= 1
    tablero[y][x] = pieza_selec

def revertir_seleccion():
    imprimir_tablero()
    global p
    print(f"\nPieza seleccionada: {pieza_selec}")
    p = input('\nIngrese la posición donde quiere mover la pieza o presione "v" para volver\n')
    if p == "v":
        reiniciar_turno()
        return True
    else:
        return False

def movimiento_pieza(p, x, y, es_jaque_actual, es_turno_blanco):
    global pieza_selec
    color = "blanco" if es_turno_blanco else "negro"
    if x == xv and y == yv:
        print("\n¡No puedes mover la pieza a su propia posición!")
        return False
    elif p in piezas_blancas and tablero[y][x] not in piezas_blancas + NR:
        if es_pieza_actual(BP): 
            mov_valido, pieza_coronada = mov_peon(color, y, x, yv, xv)
            if mov_valido and pieza_coronada:
                pieza_selec = pieza_coronada
            return mov_valido
        elif es_pieza_actual(BC):
            return mov_caballo()
        elif es_pieza_actual(BA):
            return mov_alfil()
        elif es_pieza_actual(BT):
            return mov_torre()    
        elif es_pieza_actual(BD):
            return mov_reina()
        elif es_pieza_actual(BR):
            return mov_rey(y, x, yv, xv, es_jaque_actual, es_turno_blanco)
    elif p in piezas_negras and tablero[y][x] not in piezas_negras + BR:
        if es_pieza_actual(NP): 
            mov_valido, pieza_coronada = mov_peon(color, y, x, yv, xv)
            if mov_valido and pieza_coronada:
                pieza_selec = pieza_coronada
            return mov_valido
        elif es_pieza_actual(NC):
            return mov_caballo()
        elif es_pieza_actual(NA):
            return mov_alfil()
        elif es_pieza_actual(NT):
            return mov_torre()   
        elif es_pieza_actual(ND):
            return mov_reina()
        elif es_pieza_actual(NR):
            return mov_rey(y, x, yv, xv, es_jaque_actual, es_turno_blanco)
    else:
        return False

# Inicio del juego
while True:
    imprimir_tablero()

    es_turno_blanco = turnos(turno)
    rey_actual = BR if es_turno_blanco else NR
    ya, xa = hallar_posicion_pieza(tablero, rey_actual)
    
    atacantes_jaque = detalles_jaque((ya, xa), rey_actual, es_turno_blanco)
    es_jaque_actual = len(atacantes_jaque) > 0
    if es_jaque_actual:
        if es_jaque_mate((ya, xa), es_turno_blanco, atacantes_jaque):
            print(f"\n¡Jaque mate! ¡Ganan las {'negras' if es_turno_blanco else 'blancas'}!")
            break 
        print(f"\n¡Jaque al rey {'blanco' if es_turno_blanco else 'negro'}!")
   
    p = input("\nIngrese la posición de la pieza que quiere seleccionar\n")
    
    ###### Quitar esta linea al final ######
    if p.lower() == "s":
        turno += 1
        continue
    ########################################
    
    if not es_posicion_valida(p):
        mensaje_validacion("posicion_fuera")
        continue

    pieza_selec = tablero[y][x]

    if pieza_selec in CASILLAS_VACIAS:
        mensaje_validacion("casilla_vacia")
        continue

    piezas_aliadas = piezas_blancas if es_turno_blanco else piezas_negras

    if pieza_selec not in piezas_aliadas:
        mensaje_validacion("turno_incorrecto")
        continue

    tablero[y][x] = tablero_vacio[y][x]
    xv, yv = x, y
    turno += 1
    
    while not revertir_seleccion():
        if es_posicion_valida(p) and movimiento_pieza(pieza_selec, x, y, es_jaque_actual, es_turno_blanco):
            tablero_copia = copy.deepcopy(tablero)
            tablero[y][x] = pieza_selec
            if pieza_selec != rey_actual and esta_amenazada((ya, xa), rey_actual, es_turno_blanco):
                tablero = tablero_copia
                mensaje_validacion("rey_en_jaque")
            else:
                break
        else:
            mensaje_validacion("posicion_invalida")