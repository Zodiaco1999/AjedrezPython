from PiezasYCasillas import *

fila_p = []
fila_i = []
tablero = []
tablero_vacio = []

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

# Asignando las piezas a las posciciones de la matris bidimensional 
tablero[0][0] = tablero[0][7] = TN
tablero[0][1] = tablero[0][6] = CN
tablero[0][2] = tablero[0][5] = AN
tablero[0][3] = DN
tablero[0][4] = RN
tablero[7][0] = tablero[7][7] = TB
tablero[7][1] = tablero[7][6] = CB
tablero[7][2] = tablero[7][5] = AB
tablero[7][3] = DB
tablero[4][3] = RB

for i in range(8):
    tablero[6][i] = PB
    tablero[1][i] = PN

filas_t = "12345678"
columnas_t = "abcdefgh"
x = 0
y = 0
turno = 1
turno_inv = 0
pieza_selec = ""

def msj_posicion_inv():
    print("\n¡Posición invalida!\n")
    input("Presione enter para continuar")
    
def validar_posicion(p):
    global x
    global y 
    contador = 0
    for i in p:
        if contador == 0:
            if i in columnas_t:
                if i == "a":
                    x = 0
                elif i == "b":
                    x = 1
                elif i == "c":
                    x = 2
                elif i == "d":
                    x = 3
                elif i == "e":
                    x = 4
                elif i == "f":
                    x = 5
                elif i == "g":
                    x = 6
                elif i == "h":
                    x = 7
            else:
                return False
        else:
            if i in filas_t:
                if i == "1":
                    y = 7
                elif i == "2":
                    y = 6
                elif i == "3":
                    y = 5
                elif i == "4":
                    y = 4
                elif i == "5":
                    y = 3
                elif i == "6":
                    y = 2
                elif i == "7":
                    y = 1
                elif i == "8":
                    y = 0
            else:
                return False       
        contador += 1
    return True

primer_mov_pb = 0
primer_mov_pn = 0

def turnos(t, ti=1):
    global primer_mov_pb
    global primer_mov_pn 
    if ti:
        if t % 2 != 0:
            print("\n=============Turno de las blancas===============")
            primer_mov_pb = 0
        else:
            print("\n=============Turno de las negras================")
            primer_mov_pn = 0
    else:
        if t % 2 != 0:
            print("\n¡Por favor, seleccione una pieza blanca!\n")
            input("Presione enter para continuar\n")
        else:
            print("\n¡Por favor, seleccione una pieza negra!\n")
            input("Presione enter para continuar\n")
            
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

# def recorrido_torre(list_cy, list_cx):
    
def mov_torre():
    list_cy, list_cx  = [], []
    cy, cx =  yv, xv 
    if xv == x and yv > y:
        while cy > -1:
            list_cy.append(cy)
            if cy == y:
                for i in range(len(list_cy)):
                    if (tablero[list_cy[i]][x] in all_piezas) and (i + 1 < len(list_cy)):
                        return False 
                return True 
            cy -= 1
    elif xv < x and yv == y:
        while cx < 8:
            list_cx.append(cx)
            if cx == x:
                for i in range(len(list_cx)):
                    if (tablero[y][list_cx[i]] in all_piezas) and (i + 1 < len(list_cx)):
                        return False 
                return True 
            cx += 1
    elif xv == x and yv < y:
        while cy < 8:
            list_cy.append(cy)
            if cy == y:
                for i in range(len(list_cy)):
                    if (tablero[list_cy[i]][x] in all_piezas) and (i + 1 < len(list_cy)):
                        return False 
                return True 
            cy += 1
    elif xv > x and yv == y:
        while cx > -1:
            list_cx.append(cx)
            if cx == x:
                for i in range(len(list_cx)):
                    if (tablero[y][list_cx[i]] in all_piezas) and (i + 1 < len(list_cx)):
                        return False 
                return True 
            cx -= 1  
    
def identificacion_pieza_selec(p, xv, yv, x, y):
    global primer_mov_pb
    global primer_mov_pn 
    
    incr_xv = xv + 1
    decr_xv = xv - 1

    if xv == 7:
        incr_xv = 7
    if xv == 0:
        decr_xv = 0
        
    if p in piezas_blancas and tablero[y][x] not in piezas_blancas + RN:
        # Validación movimiento de peón blanco           
        if p == PB: 
            # Validación captura el paso peón blanco
            if yv == 3 and tablero[yv][incr_xv] == PN and primer_mov_pn == 1:
                if y == 2 and incr_xv == x:
                    tablero[yv][incr_xv] = tablero_vacio[yv][incr_xv]
                    return True
            if yv == 3 and tablero[yv][decr_xv] == PN and primer_mov_pn == 1:
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
                        primer_mov_pb = 1     
                    return True    
                if yv - 1 == y and (incr_xv == x or xv - 1 == x):
                    if tablero[y][x] in piezas_negras_sr:
                        return True
        # Validación movimiento de Caballo blanco
        elif p == CB:
            return mov_caballo()
        # Validación movimiento de Alfil blanco  
        elif p == AB:
            return mov_alfil()
        elif p == TB:
            return mov_torre()    
        elif p == DB:
            return mov_alfil() or mov_torre()
        elif p == RB:
            if (xv + 1 == x or xv - 1 == x or xv == x) and (yv + 1 == y or yv - 1 == y or yv == y):
                return True         
    elif p in piezas_negras and tablero[y][x] not in piezas_negras + RB:
        # Validación movimiento de Peón negro
        if p == PN:
            # Validación captura el paso peón negro 
            if yv == 4 and tablero[yv][incr_xv] == PB and primer_mov_pb == 1:
                if y == 5 and incr_xv == x:
                    tablero[yv][incr_xv] = tablero_vacio[yv][incr_xv]
                    return True
            if yv == 4 and tablero[yv][decr_xv] == PB and primer_mov_pb == 1:
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
                        primer_mov_pn = 1 
                    return True    
                if yv + 1 == y and (xv + 1 == x or xv - 1 == x):
                    if tablero[y][x] in piezas_blancas_sr:
                        return True   
        # Validación movimiento de Caballo negro    
        elif p == CN:
            return mov_caballo()
        elif p == AN:
            return mov_alfil()
        elif p == TN:
            return mov_torre()   
        elif p == DN:
            return mov_alfil() or mov_torre()
        elif p == RN:
            if (xv + 1 == x or xv - 1 == x) or (yv + 1 == y or yv - 1 == y):
                return True
    else:
        return False
    
def volver():
    imprimir_tablero()
    global p
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
            if tablero[y][x] == RB:
                ubic_rey = tablero[y][x]
                break
        else:
            continue
        break
    
    if tablero[y - 1][x + 1] == PN or tablero[y - 1][x - 1] == PN:
        print("¡Rey blanco en jaque!")

    turnos(turno)
    p = input("\nIngrese la posición donde está actualmente la pieza que quiere seleccionar\n")
    
    if validar_posicion(p):
        if tablero[y][x] == "◻ " or tablero[y][x] == "◼ ":
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
        if not validar_posicion(p) or not identificacion_pieza_selec(pieza_selec, xv, yv, x, y):
            msj_posicion_inv()
        else: break
    tablero[y][x] = pieza_selec
    