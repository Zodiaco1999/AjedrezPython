from constantes.piezas import B, N, BP, BC, BA, BT, BR, BD, NP, NC, NA, NT, NR, ND
import copy

def asignar_casillas_tablero():
    tablero = []
    fila_p = []
    fila_i = []
    
    for t in range(4):
        for i in range(8):
            if i % 2 == 0:
                fila_p.append(B)
            else:
                fila_p.append(N)
            fila_i.insert(0, fila_p[i])
            
        tablero.append(fila_p[:8])
        tablero.append(fila_i[:8]) 
        
    return tablero

def organizar_piezas_tablero(tablero):
    # Asignando las piezas blancas
    tablero[6] = [BP] * 8
    tablero[7][1] = tablero[7][6] = BC
    tablero[7][2] = tablero[7][5] = BA
    tablero[7][0] = tablero[7][7] = BT
    tablero[7][3] = BD
    tablero[7][4] = BR
    # Asignando las piezas negras
    tablero[1] = [NP] * 8
    tablero[0][1] = tablero[0][6] = NC
    tablero[0][2] = tablero[0][5] = NA
    tablero[0][0] = tablero[0][7] = NT
    tablero[0][3] = ND
    tablero[0][4] = NR

    return tablero

def inicializar_tablero():
    tablero = asignar_casillas_tablero()
    tablero_vacio = copy.deepcopy(tablero)
    tablero = organizar_piezas_tablero(tablero)
    return tablero, tablero_vacio