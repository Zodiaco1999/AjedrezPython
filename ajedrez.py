from piezas_y_casillas import *

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
enroque_br = False
enroque_nr = False
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

# Asignando las piezas a las posciciones de la matriz bidimensional 
tablero[0][0] = tablero[0][7] = NT
tablero[0][1] = tablero[0][6] = NC
tablero[0][2] = tablero[0][5] = NA
tablero[0][3] = ND
tablero[0][4] = NR
tablero[4][3] = tablero[4][4] = BT
# tablero[7][1] = tablero[7][6] = BC
# tablero[7][2] = tablero[7][5] = BA
# tablero[7][3] = BD
tablero[7][4] = BR
tablero[6] = [BP] * 8
tablero[1] = [NP] * 8

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
    global primer_mov_bp
    global primer_mov_np 
    if ti:
        if t % 2 != 0:
            print("\n=============Turno de las blancas===============")
            primer_mov_bp = False
        else:
            print("\n=============Turno de las negras================")
            primer_mov_np = False
    else:
        if t % 2 != 0:
            print("\n¡Por favor, seleccione una pieza blanca!\n")
            input("Presione enter para continuar\n")
        else:
            print("\n¡Por favor, seleccione una pieza negra!\n")
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

def recorrido_alfil(list_cy, list_cx):
    for i in range(len(list_cx)):
        if (tablero[list_cy[i]][list_cx[i]] in all_piezas) and (i + 1 < len(list_cx)):
           return False 
    return True
    
def mov_alfil():
    # "cix" es: contador en incremento x "cdy" es: contador en disminución y
    ciy, cdy, cix, cdx = yv + 1, yv - 1, xv + 1, xv - 1
    list_cy, list_cx  = [], []
    if xv < x and yv > y:
        while cix < 8 and cdy > -1:
            list_cy.append(cdy), list_cx.append(cix)
            if cdy == y and cix == x:
                return recorrido_alfil(list_cy, list_cx)
            cdy -= 1 
            cix += 1 
    elif xv > x and yv > y: 
        while cdx > -1 and cdy > -1:
            list_cy.append(cdy), list_cx.append(cdx)
            if cdy == y and cdx == x:
                return recorrido_alfil(list_cy, list_cx)
            cdy -= 1 
            cdx -= 1 
    elif xv < x and yv < y:
        while cix < 8 and ciy < 8:
            list_cy.append(ciy), list_cx.append(cix)
            if ciy == y and cix == x:
                return recorrido_alfil(list_cy, list_cx)
            ciy += 1 
            cix += 1 
    elif xv > x and yv < y:
        while cdx > -1 and ciy < 8:
            list_cy.append(ciy), list_cx.append(cdx)
            if ciy == y and cdx == x:
                return recorrido_alfil(list_cy, list_cx)
            ciy += 1 
            cdx -= 1

def mov_torre():
    if xv != x and yv != y:
        return False

    desplazamiento_x = (x > xv) - (x < xv)
    desplazamiento_y = (y > yv) - (y < yv)

    indice_x, indice_y = xv + desplazamiento_x, yv + desplazamiento_y
    while (indice_x, indice_y) != (x, y):
        if tablero[indice_y][indice_x] in all_piezas:
            return False
        indice_x += desplazamiento_x
        indice_y += desplazamiento_y

    return True
 
def mov_reina():
    return mov_alfil() or mov_torre()

def mov_rey_blanco():
    global enroque_br, primer_mov_br
    
    if (xv + 1 == x or xv - 1 == x or xv == x) and (yv + 1 == y or yv - 1 == y or yv == y):
        primer_mov_br = True
        return True         
    elif not enroque_br and not primer_mov_br and x == xv + 2 and tablero[y][xv + 3] == BT:
        print("¡Enroque corto rey blanco!")
        tablero[y][xv + 1] = BT
        tablero[y][xv + 3] = tablero_vacio[y][xv + 3]
        enroque_br = True
        primer_mov_br = True
        return True
    elif not enroque_br and not primer_mov_br and x == xv - 2 and tablero[y][xv - 4] == BT:
        print("¡Enroque largo rey blanco!")
        tablero[y][xv - 1] = BT
        tablero[y][xv - 4] = tablero_vacio[y][xv - 4]
        enroque_br = True
        primer_mov_br = True
        return True
    
    return False

def mov_rey_negro():
    if (xv + 1 == x or xv - 1 == x or xv == x) and (yv + 1 == y or yv - 1 == y or yv == y):
        return True         
    
    return False
    
def movimiento_pieza(p, x, y):
    # movimientos de las piezas blancas
    if p in piezas_blancas and tablero[y][x] not in piezas_blancas + NR:
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
            return mov_rey_blanco()
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
    
def volver():
    imprimir_tablero()
    global p
    print(f"\nPieza seleccionada: {pieza_selec}")
    p = input("\nIngrese la posición donde quiere mover la pieza o presione \"v\" para volver\n")
    if p == "v":
        global turno
        global x
        global y
        x = xv
        y = yv
        turno -= 1
        return True
    else:
        return False

# Inicio del juego
while True:
    imprimir_tablero()

    for y in range(8):
        for x in range(8):
            if tablero[y][x] == BR:
                ubic_rey = tablero[y][x]
                break
        else:
            continue
        break
    
    if tablero[y - 1][x + 1] == NP or tablero[y - 1][x - 1] == NP:
        print("¡Rey blanco en jaque!")

    turnos(turno)
    p = input("\nIngrese la posición de la pieza que quiere seleccionar\n")
    
    if es_posicion_valida(p):
        if tablero[y][x] == B or tablero[y][x] == N:
            print("\n¡No ha seleccionado ninguna pieza!")
            input("\nPresione enter para continuar")
            continue
        else:
            pieza_selec = tablero[y][x]
            if turno % 2 != 0:
                if pieza_selec in piezas_blancas:
                    tablero[y][x] = tablero_vacio[y][x]
                    xv = x
                    yv = y 
                else:
                    turnos(turno, turno_inv)
                    continue
            else:
                if pieza_selec in piezas_negras:
                    tablero[y][x] = tablero_vacio[y][x]
                    xv = x
                    yv = y 
                else:
                    turnos(turno, turno_inv)
                    continue
            turno += 1
    else:
        msj_posicion_inv()
        continue
    
    while not volver():
        if not es_posicion_valida(p) or not movimiento_pieza(pieza_selec, x, y):
            msj_posicion_inv()
        else: break
    tablero[y][x] = pieza_selec