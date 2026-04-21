from constantes.piezas import BP, NP, BR, NR, CASILLAS_VACIAS, PIEZAS_BLANCAS, PIEZAS_NEGRAS
from estado.estados_piezas import config_peon, guardar_estado_global
from reglas.detector_jaque import detalles_jaque, es_jaque_mate, esta_amenazada
from reglas.detector_rey_ahogado import esta_rey_ahogado
from reglas.movimientos_piezas import movimiento_pieza
from reglas.logica_coronacion import coronar_peon
from presentacion.mensajes import mensaje_validacion
from presentacion.renderizador import imprimir_tablero
from presentacion.tablero import inicializar_tablero
from utilidades.validaciones_basicas import posicion_valida
from utilidades.buscador_piezas import hallar_posicion_pieza
from juego.gestor_turnos import turnos
import copy

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

        resultado = posicion_valida(p)
        if not resultado:
            mensaje_validacion("posicion_fuera")
            continue

        y, x = resultado
        pieza_selec = tablero[y][x]

        if pieza_selec in CASILLAS_VACIAS:
            mensaje_validacion("casilla_vacia")
            continue

        piezas_aliadas = PIEZAS_BLANCAS if es_turno_blanco else PIEZAS_NEGRAS

        if pieza_selec not in piezas_aliadas:
            mensaje_validacion("turno_incorrecto")
            continue

        tablero[y][x] = tablero_vacio[y][x]
        xv, yv = x, y

        if elegir_posicion(tablero, tablero_vacio, pieza_selec, yv, xv, y, x, es_turno_blanco, es_jaque_actual, rey_actual, (yr, xr)):
            turno += 1
