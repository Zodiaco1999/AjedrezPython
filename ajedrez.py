from piezas_y_casillas import *
from movimientos import *
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
turno_inv = 0
pieza_selec = ""
primer_mov_bp = False
primer_mov_np = False
primer_mov_nr = False
primer_mov_ntd = False
primer_mov_nti = False
primer_mov_br = False
primer_mov_btd = False
primer_mov_bti = False

# tablero = [[N for i in range(8) if i % 2 == 0] for j in range(8)]

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
#tablero[6] = [BP] * 8
#tablero[7][1] = tablero[7][6] = BC
#tablero[7][2] = tablero[7][5] = BA
tablero[7][0] = tablero[1][1] = BT
#tablero[7][3] = BD
tablero[7][6] = BR
# Asignando las piezas negras
#tablero[1] = [NP] * 8
tablero[0][1] = tablero[0][6] = NC
tablero[0][2] = tablero[0][5] = NA
tablero[0][0] = tablero[7][1] = NT
tablero[1][0] = ND
tablero[0][3] = NR

def msj_posicion_inv():
    print("\n¡Posición invalida!\n")
    input("Presione enter para continuar")
    
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

def turnos(t, ti=1):
    global primer_mov_bp, primer_mov_np
    
    es_turno_blanco = t % 2 != 0
    color = "blanca" if es_turno_blanco else "negra"
    
    print(f"\n================Turno de las {color}s================")
    if es_turno_blanco: 
        primer_mov_bp = False
        return True
    else: 
        primer_mov_np = False
        return False
            
def turno_invalido(es_turno_blanco):
    color = "blanca" if es_turno_blanco else "negra"
    print(f"\n¡Por favor, seleccione una pieza {color}!\n")
    input("Presione enter para continuar\n")
    
def es_pieza_actual(pieza):
    return pieza_selec == pieza
            
def mov_peon_blanco():
    global primer_mov_bp, primer_mov_np 
    incr_xv = xv + 1
    decr_xv = xv - 1

    if xv == 7:
        incr_xv = 7
    if xv == 0:
        decr_xv = 0
    
    # Validación captura el paso peón blanco
    if yv == 3 and tablero[yv][incr_xv] == NP and primer_mov_np:
        if y == 2 and incr_xv == x:
            tablero[yv][incr_xv] = tablero_vacio[yv][incr_xv]
            return True
    if yv == 3 and tablero[yv][decr_xv] == NP and primer_mov_np:
        if y == 2 and decr_xv == x:
            tablero[yv][decr_xv] = tablero_vacio[yv][decr_xv]
            return True
    # --------------------------------------
    if yv in range(6):
        if yv - 1 == y and xv == x and tablero[y][x] not in all_piezas:  
            return True
        elif yv - 1 == y and xv + 1 == x or xv - 1 == x:
            if tablero[y][x] in piezas_negras_sr:
                return True
    else:
        if ((yv - 2 == y or yv - 1 == y) and xv == x) and tablero[y][x] not in all_piezas:
            if y == 4:
                primer_mov_bp = True     
            return True    
        if yv - 1 == y and (incr_xv == x or xv - 1 == x):
            if tablero[y][x] in piezas_negras_sr:
                return True
        
def mov_peon_negro():
    global primer_mov_bp, primer_mov_np 
    incr_xv = xv + 1
    decr_xv = xv - 1

    if xv == 7:
        incr_xv = 7
    if xv == 0:
        decr_xv = 0
    
    # Validación captura el paso peón negro 
    if yv == 4 and tablero[yv][incr_xv] == BP and primer_mov_bp:
        if y == 5 and incr_xv == x:
            tablero[yv][incr_xv] = tablero_vacio[yv][incr_xv]
            return True
    if yv == 4 and tablero[yv][decr_xv] == BP and primer_mov_bp:
        if y == 5 and decr_xv == x:
            tablero[yv][decr_xv] = tablero_vacio[yv][decr_xv]
            return True
    # -------------------------------------    
    if yv in range(2, 8):
        if yv + 1 == y and xv == x and tablero[y][x] not in all_piezas:  
           return True
        elif yv + 1 == y and xv + 1 == x or xv - 1 == x:
           if tablero[y][x] in piezas_blancas_sr:
               return True    
    else:
        if ((yv + 2 == y or yv + 1 == y) and xv == x) and tablero[y][x] not in all_piezas: 
            if y == 3:
                primer_mov_np = True 
            return True    
        if yv + 1 == y and (xv + 1 == x or xv - 1 == x):
            if tablero[y][x] in piezas_blancas_sr:
                return True   
         
def mov_caballo():
    if ((xv + 2 == x or xv - 2 == x) and (yv - 1 == y or yv + 1 == y)) or ((xv + 1 == x or xv - 1 == x) and (yv - 2 == y or yv + 2 == y)):
        return True

def camino_libre():
    desplazamiento_x = (x > xv) - (x < xv)
    desplazamiento_y = (y > yv) - (y < yv)

    indice_x = xv + desplazamiento_x 
    indice_y = yv + desplazamiento_y
    
    while (indice_y, indice_x) != (y, x):
        if tablero[indice_y][indice_x] in all_piezas:
            return False
        indice_x += desplazamiento_x
        indice_y += desplazamiento_y

    return True
    
def mov_alfil():
    if abs(x - xv) != abs(y - yv):
        return False

    return camino_libre()
 
def mov_torre():
    global primer_mov_nti, primer_mov_ntd, primer_mov_bti, primer_mov_btd
    if xv != x and yv != y:
        return False
    
    es_movimiento_valido = camino_libre()
    
    if es_movimiento_valido:
        if (yv, xv) == (0, 0):
            primer_mov_nti = True
        elif (yv, xv) == (0, 7):
            primer_mov_ntd = True
        elif (yv, xv) == (7, 0):
            primer_mov_bti = True
        elif (yv, xv) == (7, 7):
            primer_mov_btd = True 

    return es_movimiento_valido
 
def mov_reina():
    return mov_alfil() or mov_torre()

def mov_rey_blanco(es_jaque_actual):
    global primer_mov_br
    
    if abs(x - xv) <= 1 and abs(y - yv) <= 1: 
        if es_jaque((y, x), True):
            print("\n¡No puedes mover el rey a esa posición porque estaría en jaque!")
            return False

        for dy, dx in MOVIMIENTOS_REY:
            yn, xn = y + dy, x + dx
            if validar_jaque(yn, xn, NR):
                print("\n¡No puedes mover el rey a esa posición porque estaría en jaque!")
                return False

        primer_mov_br = True
        return True             
    elif not es_jaque_actual and not primer_mov_br and not primer_mov_btd and tablero[y][xv + 1] in CASILLAS_VACIAS and x == xv + 2 and tablero[y][xv + 3] == BT:
        for dx in range(1, 3):
            if es_jaque((y, xv + dx), True):
                print("\n¡No puedes enrocar porque el rey pasaría por una casilla en jaque!")
                return False
            
        print("\n¡Enroque corto rey blanco!")
        tablero[y][xv + 1] = BT
        tablero[y][xv + 3] = tablero_vacio[y][xv + 3]
        primer_mov_br = True
        return True
    elif (not es_jaque_actual and not primer_mov_br and not primer_mov_bti and 
          tablero[y][xv - 1] in CASILLAS_VACIAS and tablero[y][xv - 3] in CASILLAS_VACIAS 
          and x == xv - 2 and tablero[y][xv - 4] == BT):
        for dx in range(1, 3):
            if es_jaque((y, xv - dx), True):
                print("\n¡No puedes enrocar porque el rey pasaría por una casilla en jaque!")
                return False
            
        print("\n¡Enroque largo rey blanco!")
        tablero[y][xv - 1] = BT
        tablero[y][xv - 4] = tablero_vacio[y][xv - 4]
        primer_mov_br = True
        return True
    
    return False

def mov_rey_negro():
    global primer_mov_nr
    
    if (xv + 1 == x or xv - 1 == x or xv == x) and (yv + 1 == y or yv - 1 == y or yv == y):
        primer_mov_nr = True
        return True         
    elif not primer_mov_nr and x == xv + 2 and tablero[y][xv + 3] == NT:
        print("¡Enroque corto rey negro!")
        tablero[y][xv + 1] = NT
        tablero[y][xv + 3] = tablero_vacio[y][xv + 3]
        primer_mov_nr = True
        return True
    elif not primer_mov_nr and x == xv - 2 and tablero[y][xv - 4] == NT:
        print("¡Enroque largo rey negro!")
        tablero[y][xv - 1] = NT
        tablero[y][xv - 4] = tablero_vacio[y][xv - 4]
        primer_mov_nr = True
        return True
    
    return False
    
def movimiento_pieza(p, x, y, es_jaque_actual):
    if x == xv and y == yv:
        print("\n¡No puedes mover la pieza a su propia posición!")
        return False
    # movimientos de las piezas blancas
    elif p in piezas_blancas and tablero[y][x] not in piezas_blancas + NR:
        if es_pieza_actual(BP): 
            return mov_peon_blanco()
        elif es_pieza_actual(BC):
            return mov_caballo()
        elif es_pieza_actual(BA):
            return mov_alfil()
        elif es_pieza_actual(BT):
            return mov_torre()    
        elif es_pieza_actual(BD):
            return mov_reina()
        elif es_pieza_actual(BR):
            return mov_rey_blanco(es_jaque_actual)
    # movimientos de las piezas negras        
    elif p in piezas_negras and tablero[y][x] not in piezas_negras + BR:
        if es_pieza_actual(NP):
            return mov_peon_negro()
        elif es_pieza_actual(NC):
            return mov_caballo()
        elif es_pieza_actual(NA):
            return mov_alfil()
        elif es_pieza_actual(NT):
            return mov_torre()   
        elif es_pieza_actual(ND):
            return mov_reina()
        elif es_pieza_actual(NR):
            return mov_rey_negro()
    else:
        return False
    
def hallar_posicion_pieza(tablero, pieza_buscada):
    for y, fila in enumerate(tablero):
        if pieza_buscada in fila:
            x = fila.index(pieza_buscada)
            return [y, x]
    return None
    
def validar_jaque(yn, xn, pieza_objetivo):
    return 0 <= yn < 8 and 0 <= xn < 8 and tablero[yn][xn] == pieza_objetivo

def movimientos_estrella(posicion_rey, movimientos, atacantes_validos):
    ya, xa = posicion_rey
    for dy, dx in movimientos:
        yn, xn = ya + dy, xa + dx
        
        while 0 <= yn < 8 and 0 <= xn < 8:
            pieza_actual = tablero[yn][xn]
            
            if pieza_actual not in CASILLAS_VACIAS:
                if pieza_actual in atacantes_validos:
                    return True
                break 
                
            yn += dy
            xn += dx
            
    return False

def es_jaque(posicion_rey, es_turno_blanco):
    ya, xa = posicion_rey
    peon_rival = NP if es_turno_blanco else BP
    caballo_rival = NC if es_turno_blanco else BC
    alfil_rival = NA if es_turno_blanco else BA
    torre_rival = NT if es_turno_blanco else BT
    dama_rival = ND if es_turno_blanco else BD
    movimientos_peon_rival = MOVIMIENTOS_PEON_NEGRO if es_turno_blanco else MOVIMIENTOS_PEON_BLANCO

    for dy, dx in movimientos_peon_rival:
        if validar_jaque(ya + dy, xa + dx, peon_rival):
            return True

    for dy, dx in MOVIMIENTOS_CABALLO:
        if validar_jaque(ya + dy, xa + dx, caballo_rival):
            return True
            
    atacantes_diagonales = {alfil_rival, dama_rival}
    if movimientos_estrella((ya, xa), MOVIMIENTOS_ALFIL, atacantes_diagonales):
        return True

    atacantes_ortogonales = {torre_rival, dama_rival}
    if movimientos_estrella((ya, xa), MOVIMIENTOS_TORRE, atacantes_ortogonales):
        return True

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

# Inicio del juego
while True:
    imprimir_tablero()

    es_turno_blanco = turnos(turno)
    rey_actual = BR if es_turno_blanco else NR
    ya, xa = hallar_posicion_pieza(tablero, rey_actual)
    
    es_jaque_actual = es_jaque((ya, xa), es_turno_blanco)
    if es_jaque_actual:
        print(f"\n¡Jaque al rey {'blanco' if es_turno_blanco else 'negro'}!")
    
    p = input("\nIngrese la posición de la pieza que quiere seleccionar\n")
    
    ###### Quitar esta linea al final ######
    if p.lower() == "s":
        turno += 1
        continue
    ########################################
    
    if es_posicion_valida(p):
        pieza_selec = tablero[y][x]
        if pieza_selec in CASILLAS_VACIAS:
            print("\n¡No ha seleccionado ninguna pieza!")
            input("\nPresione enter para continuar")
            continue
        else:
            if es_turno_blanco:
                if pieza_selec in piezas_blancas:
                    tablero[y][x] = tablero_vacio[y][x]
                    xv = x
                    yv = y 
                else:
                    turno_invalido(es_turno_blanco)
                    continue
            else:
                if pieza_selec in piezas_negras:
                    tablero[y][x] = tablero_vacio[y][x]
                    xv = x
                    yv = y 
                else:
                    turno_invalido(es_turno_blanco)
                    continue
            turno += 1
    else:
        msj_posicion_inv()
        continue
    
    while not revertir_seleccion():
        if es_posicion_valida(p) and movimiento_pieza(pieza_selec, x, y, es_jaque_actual):
            tablero_copia = copy.deepcopy(tablero)
            tablero[y][x] = pieza_selec
            if es_jaque((y, x) if pieza_selec == rey_actual else (ya, xa), es_turno_blanco):
                tablero = tablero_copia
                print("\n¡No puedes mover ahí porque tu rey estaría en jaque!")
                msj_posicion_inv()
            else:
                break
        else:
            msj_posicion_inv()
    