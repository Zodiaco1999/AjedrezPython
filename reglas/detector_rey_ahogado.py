from constantes.piezas import PIEZAS_BLANCAS, PIEZAS_NEGRAS
from diccionarios.mapeos import MOVIMIENTOS_POR_PIEZA
from utilidades.buscador_piezas import hallar_posicion_piezas
from utilidades.validaciones_basicas import es_coordenada_valida
from reglas.detector_jaque import esta_amenazada
from reglas.movimientos_piezas import movimiento_pieza
import copy

def esta_rey_ahogado(tablero, tablero_vacio, es_turno_blanco, rey_actual, posicion_rey):
    piezas_actuales_str = PIEZAS_BLANCAS if es_turno_blanco else PIEZAS_NEGRAS
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