from piezas_y_casillas_const import *
from movimientos_const import *
from validaciones import *
from movimientos import *
import copy

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
turno = 1

# LLenar los tableros con las casillas negras y blancas
def inicializar_tablero():
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

def nomenclatura_columnas():
    print("    A     B     C     D     E     F     G     H")   
       
# Imprimir el tablero en orden 
def imprimir_tablero(tablero):
    print()
    nomenclatura_columnas()
    for i in range(8):
        print(8 - i,tablero[i][:],8 - i)
    nomenclatura_columnas()


def organizar_piezas_tablero(tablero):
    # Asignando las piezas blancas
    tablero[6] = [BP] * 8
    tablero[7][1] = tablero[4][4] = BC
    tablero[7][2] = tablero[7][5] = BA
    tablero[7][0] = tablero[7][7] = BT
    tablero[2][7] = BD
    tablero[1][7] = BR
    # Asignando las piezas negras
    #tablero[1] = [NP] * 8
    # tablero[0][1] = tablero[0][6] = NC
    # tablero[0][2] = tablero[0][5] = NA
    # tablero[0][0] = tablero[0][7] = NT
    # tablero[0][7] = ND
    tablero[1][1] = NR
    tablero[1][6] = BP
    tablero[1][5] = NT
    
    return tablero
    

def coronar_peon(es_turno_blanco):
    piezas_coronacion = f"d){BD}, t){BT}, a){BA}, c){BC}" if es_turno_blanco else f"d){ND}, t){NT}, a){NA}, c){NC}"
    print("\n¡Tu peón ha llegado al final del tablero!")
    
    selec_pieza_coronada = None
    while selec_pieza_coronada not in ['c', 'a', 't', 'd']:
        selec_pieza_coronada = input(f"Ingresa la pieza que deseas coronar\n{piezas_coronacion} ").lower()
    
    mapeo_piezas = {
        'c': BC if es_turno_blanco else NC,
        'a': BA if es_turno_blanco else NA,
        't': BT if es_turno_blanco else NT,
        'd': BD if es_turno_blanco else ND
    }
    
    return mapeo_piezas[selec_pieza_coronada]

def esta_rey_ahogado(tablero, es_turno_blanco, rey_actual, posicion_rey, es_jaque_actual):
    piezas_actuales_str = piezas_blancas if es_turno_blanco else piezas_negras
    piezas_actuales = [piezas_actuales_str[i:i+2] for i in range(0, len(piezas_actuales_str), 2)] 
    movimientos_dic = {
        BP: MOVIMIENTOS_PEON_BLANCO, NP: MOVIMIENTOS_PEON_NEGRO,
        BC: MOVIMIENTOS_CABALLO, NC: MOVIMIENTOS_CABALLO,
        BA: MOVIMIENTOS_ALFIL, NA: MOVIMIENTOS_ALFIL,
        BT: MOVIMIENTOS_TORRE, NT: MOVIMIENTOS_TORRE,
        BD: MOVIMIENTOS_TORRE + MOVIMIENTOS_ALFIL, ND: MOVIMIENTOS_TORRE + MOVIMIENTOS_ALFIL,
        BR: MOVIMIENTOS_REY, NR: MOVIMIENTOS_REY,
    }
    yr, xr = posicion_rey
    tablero_copia = copy.deepcopy(tablero)
    
    for pieza in piezas_actuales:
        posiciones_piezas = hallar_posicion_piezas(tablero, pieza)
        if not posiciones_piezas:
            continue
        
        for ya, xa in posiciones_piezas:
            for dy, dx in movimientos_dic[pieza]:
                tablero[:] = tablero_copia
                yn, xn = ya + dy, xa + dx
                tablero[ya][xa] = tablero_vacio[ya][xa]
                if es_coordenada_valida(yn, xn) and movimiento_pieza(tablero, pieza, xn, yn, xa, ya, es_jaque_actual, es_turno_blanco): 
                    tablero[yn][xn] = pieza 
                    if pieza != rey_actual and esta_amenazada(tablero, (yr, xr), rey_actual, es_turno_blanco):
                        continue
                    
                    return False
                
    tablero[:] = tablero_copia  
        
    return True

def turnos(t):
    es_turno_blanco = t % 2 != 0
    color = "blanco" if es_turno_blanco else "negro"
    estado_peones[color]['salto_doble'] = False
    estado_peones[color]['columna'] = None
    
    print(f"\n================Turno de las {'blancas' if es_turno_blanco else 'negras'}================")
    return es_turno_blanco

def hallar_posicion_pieza(tablero, pieza_buscada):
    for y, fila in enumerate(tablero):
        if pieza_buscada in fila:
            x = fila.index(pieza_buscada)
            return [y, x]
    return None

def hallar_posicion_piezas(tablero, pieza_buscada):
    piezas_encontradas = []
    for y, fila in enumerate(tablero):
        for x, pieza in enumerate(fila):
            if pieza == pieza_buscada:
                piezas_encontradas.append((y, x))
            
    return piezas_encontradas if piezas_encontradas else None

def posicion_valida(p):
    if len(p) != 2:
        return False
    
    p = p.lower() 
    
    x = columnas_a_indices.get(p[0])
    y = filas_a_indices.get(p[1])
    
    if x is None or y is None:
        return None
    
    return y, x

def movimiento_pieza(tablero, tablero_vacio, p, x, y, xv, yv, es_jaque_actual, es_turno_blanco):
    global pieza_selec
    color = "blanco" if es_turno_blanco else "negro"
    
    if x == xv and y == yv:
        print("\n¡No puedes mover la pieza a su propia posición!")
        return False
    
    if not ((p in piezas_blancas and tablero[y][x] not in piezas_blancas + NR) or 
            (p in piezas_negras and tablero[y][x] not in piezas_negras + BR)):
        return False

    movimientos_piezas = {
        BP: lambda: mov_peon(tablero, tablero_vacio, color, y, x, yv, xv),
        NP: lambda: mov_peon(tablero, tablero_vacio, color, y, x, yv, xv),
        BC: lambda: mov_caballo(y, x, yv, xv),
        NC: lambda: mov_caballo(y, x, yv, xv),
        BA: lambda: mov_alfil(tablero, y, x, yv, xv),
        NA: lambda: mov_alfil(tablero, y, x, yv, xv),
        BT: lambda: mov_torre(tablero, y, x, yv, xv),
        NT: lambda: mov_torre(tablero, y, x, yv, xv),
        BD: lambda: mov_reina(tablero, y, x, yv, xv),
        ND: lambda: mov_reina(tablero, y, x, yv, xv),
        BR: lambda: mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco),
        NR: lambda: mov_rey(tablero, tablero_vacio, y, x, yv, xv, es_jaque_actual, es_turno_blanco),
    }

    return movimientos_piezas[p]()

def elegir_posicion(tablero, tablero_vacio, pieza_selec, es_turno_blanco):
    while True:
        imprimir_tablero(tablero)
        print(f"\nPieza seleccionada: {pieza_selec}")
        p = input('\nIngrese la posición donde quiere mover la pieza o presione "v" para volver\n')
        
        if p == "v":
            tablero[yv][xv] = pieza_selec
            return False
        
        resultado = posicion_valida(p)
        if not resultado:
            mensaje_validacion("posicion_invalida")
            continue
        
        y, x = resultado
        if movimiento_pieza(tablero, tablero_vacio, pieza_selec, x, y, xv, yv, es_jaque_actual, es_turno_blanco):
            tablero_copia = copy.deepcopy(tablero)
            if pieza_selec in {BP, NP}:
                color = "blanco" if es_turno_blanco else "negro"
                if config_peon[color]['coronacion'] == y: 
                    pieza_coronada = coronar_peon(es_turno_blanco)
                    pieza_selec = pieza_coronada
            tablero[y][x] = pieza_selec 
            if pieza_selec != rey_actual and esta_amenazada((ya, xa), rey_actual, es_turno_blanco):
                tablero[:] = tablero_copia  
                mensaje_validacion("rey_en_jaque")
                continue
            
            return True 
        else:
            mensaje_validacion("posicion_invalida")

# Inicio del juego
while True:
    tablero = inicializar_tablero();
    tablero_vacio = copy.deepcopy(tablero)
    tablero = organizar_piezas_tablero(tablero)
    imprimir_tablero(tablero)

    es_turno_blanco = turnos(turno)
    rey_actual = BR if es_turno_blanco else NR
    ya, xa = hallar_posicion_pieza(tablero, rey_actual)
    
    atacantes_jaque = detalles_jaque(tablero, (ya, xa), rey_actual, es_turno_blanco)
    es_jaque_actual = len(atacantes_jaque) > 0
    if es_jaque_actual:
        if es_jaque_mate(tablero, (ya, xa), es_turno_blanco, atacantes_jaque):
            print(f"\n¡Jaque mate! ¡Ganan las {'negras' if es_turno_blanco else 'blancas'}!")
            break 
        print(f"\n¡Jaque al rey {'blanco' if es_turno_blanco else 'negro'}!")
   
    if not es_jaque_actual and esta_rey_ahogado(tablero, es_turno_blanco, rey_actual, (ya, xa), es_jaque_actual):
        print(f"\n¡Rey {'negro' if es_turno_blanco else 'blanco'} ahogado!, ¡Partida en tablas!")
        break
        
    p = input("\nIngrese la posición de la pieza que quiere seleccionar\n")
    
    ###### Quitar esta linea al final ######
    if p.lower() == "s":
        turno += 1
        continue
    ########################################
    
    resultado = posicion_valida(p)
    if not resultado:
        mensaje_validacion("posicion_fuera")
        continue

    y, x = resultado
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

    if elegir_posicion(tablero, tablero_vacio, pieza_selec, es_turno_blanco):
        turno += 1
    else:
        continue