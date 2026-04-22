from constantes.piezas import BP, NP, BR, NR, TOTAL_PIEZAS_SR
from estado.estados_piezas import config_peon, guardar_estado_global
from reglas.detector_jaque import detalles_jaque, es_jaque_mate, esta_amenazada
from reglas.detector_rey_ahogado import esta_rey_ahogado
from reglas.detector_repeticion import registrar_posicion, hay_repeticion_triple
from reglas.detector_cincuenta_movimientos import verificar_movimiento, hay_cincuenta_movimientos
from reglas.detector_insuficiencia_material import hay_insuficiencia_material
from reglas.movimientos_piezas import movimiento_pieza
from reglas.logica_coronacion import coronar_peon
from presentacion.mensajes import mensaje_validacion
from presentacion.renderizador import imprimir_tablero
from presentacion.tablero import inicializar_tablero
from utilidades.validaciones_basicas import posicion_valida, validar_seleccion, solicitar_posicion_pieza
from utilidades.buscador_piezas import hallar_posicion_pieza
from juego.gestor_turnos import turnos
import copy

def obtener_turno_actual(turno):
    es_turno_blanco = turnos(turno)
    rey_actual = BR if es_turno_blanco else NR
    return es_turno_blanco, rey_actual

def verificar_estado_partida(tablero, tablero_vacio, es_turno_blanco, rey_actual, posicion_rey, es_jaque_actual, atacantes_jaque):
    if es_jaque_actual:
        if es_jaque_mate(tablero, posicion_rey, es_turno_blanco, atacantes_jaque):
            return True, f"\n¡Jaque mate! ¡Ganan las {'negras' if es_turno_blanco else 'blancas'}!"
        return False, f"\n¡Jaque al rey {'blanco' if es_turno_blanco else 'negro'}!"
    
    with guardar_estado_global():
        if not es_jaque_actual and esta_rey_ahogado(tablero, tablero_vacio, es_turno_blanco, rey_actual, posicion_rey):
            return True, f"\n¡Rey {'blanco' if es_turno_blanco else 'negro'} ahogado!, ¡Partida en tablas!"
    return False, None

def realizar_movimiento(tablero, tablero_vacio, pieza_selec, yv, xv, y, x, es_turno_blanco, es_jaque_actual, rey_actual, posicion_rey):
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
            if pieza_selec != rey_actual and esta_amenazada(tablero_copia, posicion_rey, rey_actual, es_turno_blanco, con_movimientos_rey=False):
                mensaje_validacion("rey_en_jaque")
                continue
            
            hay_captura = tablero[y][x] in TOTAL_PIEZAS_SR
            tablero[y][x] = pieza_selec
            verificar_movimiento(pieza_selec, hay_captura)
            return True 
        else:
            mensaje_validacion("posicion_invalida")

def gestionar_post_movimiento(tablero, es_turno_blanco):
    registrar_posicion(tablero, es_turno_blanco)
    if hay_repeticion_triple(tablero, es_turno_blanco):
        return True, f"\n¡Posición repetida 3 veces!, ¡Partida en tablas!"
    if hay_cincuenta_movimientos():
        return True, f"\n¡Se alcanzaron 50 movimientos sin captura ni movimiento de peon!, ¡Partida en tablas!"
    if hay_insuficiencia_material(tablero):
        return True, f"\n¡Insuficiencia de material!, ¡Partida en tablas!"
    return False, None

def iniciar_juego():
    turno = 1
    tablero, tablero_vacio = inicializar_tablero()
    registrar_posicion(tablero, True)
    while True:
        imprimir_tablero(tablero)
        es_turno_blanco, rey_actual = obtener_turno_actual(turno)
        posicion_rey = hallar_posicion_pieza(tablero, rey_actual)
        atacantes_jaque = detalles_jaque(tablero, posicion_rey, rey_actual, es_turno_blanco)
        es_jaque_actual = len(atacantes_jaque) > 0
        final, mensaje = verificar_estado_partida(tablero, tablero_vacio, es_turno_blanco, rey_actual, posicion_rey, es_jaque_actual, atacantes_jaque)
        
        if mensaje:
            print(mensaje)
        if final:
            break

        pos = solicitar_posicion_pieza()
        
        if not pos:
            continue
        y, x = pos
        pieza_selec = tablero[y][x]
        
        if not validar_seleccion(pieza_selec, es_turno_blanco):
            continue
        tablero[y][x] = tablero_vacio[y][x]
        xv, yv = x, y
        
        if realizar_movimiento(tablero, tablero_vacio, pieza_selec, y, x, xv, yv, es_turno_blanco, es_jaque_actual, rey_actual, posicion_rey):
            partida_tablas, mensaje = gestionar_post_movimiento(tablero, es_turno_blanco)
            if partida_tablas:
                imprimir_tablero(tablero)
                print(f"{mensaje}\n")
                break
            turno += 1