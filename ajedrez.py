from piezas_y_casillas_const import *
from validaciones import mensaje_validacion, posicion_valida, detalles_jaque, es_jaque_mate, hallar_posicion_piezas, es_coordenada_valida
from movimientos import *
from movimientos_const import MOVIMIENTOS_POR_PIEZA
from diccionarios import estado_enroque, estado_peones, config_peon
from contextlib import contextmanager
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

def nomenclatura_columnas():
    print("    A     B     C     D     E     F     G     H")   
       
def imprimir_tablero(tablero):
    print()
    nomenclatura_columnas()
    for i in range(8):
        print(8 - i,tablero[i][:],8 - i)
    nomenclatura_columnas()

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

def esta_rey_ahogado(tablero, tablero_vacio, es_turno_blanco, rey_actual, posicion_rey):
    piezas_actuales_str = piezas_blancas if es_turno_blanco else piezas_negras
    piezas_actuales = [piezas_actuales_str[i:i+2] for i in range(0, len(piezas_actuales_str), 2)] 

    for pieza in piezas_actuales:
        posiciones_piezas = hallar_posicion_piezas(tablero, pieza)
        if not posiciones_piezas:
            continue
        
        for ya, xa in posiciones_piezas:
            for dy, dx in MOVIMIENTOS_POR_PIEZA[pieza]:
                yn, xn = ya + dy, xa + dx
                if not es_coordenada_valida(yn, xn):
                    continue
                
                tablero_copia = copy.deepcopy(tablero)
                tablero_copia[ya][xa] = tablero_vacio[ya][xa]
                if movimiento_pieza(tablero_copia, tablero_vacio, pieza, xn, yn, xa, ya, False, es_turno_blanco, True): 
                    tablero_copia[yn][xn] = pieza 
                    if pieza != rey_actual and esta_amenazada(tablero_copia, posicion_rey, rey_actual, es_turno_blanco):
                        continue
                    
                    return False
                    
    return True

def movimiento_pieza(tablero, tablero_vacio, p, x, y, xv, yv, es_jaque_actual, es_turno_blanco, es_simulacion=False):
    global pieza_selec
    color = "blanco" if es_turno_blanco else "negro"
    
    if x == xv and y == yv:
        print("\n¡No puedes mover la pieza a su propia posición!")
        return False
    
    if not ((p in piezas_blancas and tablero[y][x] not in piezas_blancas + NR) or 
            (p in piezas_negras and tablero[y][x] not in piezas_negras + BR)):
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

def elegir_posicion(tablero, tablero_vacio, pieza_selec, yv, xv, y, x, es_turno_blanco, es_jaque_actual, rey_actual, posicion_rey):
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
            color = "blanco" if es_turno_blanco else "negro"
            if pieza_selec in {BP, NP} and config_peon[color]['coronacion'] == y: 
                pieza_coronada = coronar_peon(es_turno_blanco)
                pieza_selec = pieza_coronada
            tablero_copia = copy.deepcopy(tablero)    
            tablero_copia[y][x] = pieza_selec
            if pieza_selec != rey_actual and esta_amenazada(tablero_copia, posicion_rey, rey_actual, es_turno_blanco):
                mensaje_validacion("rey_en_jaque")
                continue
            
            tablero[y][x] = pieza_selec 
            return True 
        else:
            mensaje_validacion("posicion_invalida")

@contextmanager
def guardar_estado_global():
    estado_peones_backup = copy.deepcopy(estado_peones)
    estado_enroque_backup = copy.deepcopy(estado_enroque)
    
    try:
        yield
    finally:
        estado_peones.clear()
        estado_peones.update(estado_peones_backup)
        estado_enroque.clear()
        estado_enroque.update(estado_enroque_backup)

def inicializar_tablero():
    tablero = asignar_casillas_tablero();
    tablero_vacio = copy.deepcopy(tablero)
    tablero = organizar_piezas_tablero(tablero)
    return tablero, tablero_vacio

def iniciar_juego():
    turno = 1
    tablero, tablero_vacio = inicializar_tablero()
    while True:
        imprimir_tablero(tablero)

        es_turno_blanco = turnos(turno)
        rey_actual = BR if es_turno_blanco else NR
        yr, xr = hallar_posicion_pieza(tablero, rey_actual)

        atacantes_jaque = detalles_jaque(tablero, (yr, xr), rey_actual, es_turno_blanco)
        es_jaque_actual = len(atacantes_jaque) > 0
        if es_jaque_actual:
            if es_jaque_mate(tablero, (yr, xr), es_turno_blanco, atacantes_jaque):
                print(f"\n¡Jaque mate! ¡Ganan las {'negras' if es_turno_blanco else 'blancas'}!")
                break 
            print(f"\n¡Jaque al rey {'blanco' if es_turno_blanco else 'negro'}!")
    
        with guardar_estado_global():
            if not es_jaque_actual and esta_rey_ahogado(tablero, tablero_vacio, es_turno_blanco, rey_actual, (yr, xr)):
                print(f"\n¡Rey {'blanco' if es_turno_blanco else 'negro'} ahogado!, ¡Partida en tablas!")
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

        if elegir_posicion(tablero, tablero_vacio, pieza_selec, yv, xv, y, x, es_turno_blanco, es_jaque_actual, rey_actual, (yr, xr)):
            turno += 1

iniciar_juego()