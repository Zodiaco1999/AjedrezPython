from diccionarios.mapeos import columnas_a_indices, filas_a_indices
from constantes.piezas import CASILLAS_VACIAS, PIEZAS_BLANCAS, PIEZAS_NEGRAS
from presentacion.mensajes import mensaje_validacion

def posicion_valida(p):
    if len(p) != 2:
        return False
    
    p = p.lower() 
    
    x = columnas_a_indices.get(p[0])
    y = filas_a_indices.get(p[1])
    
    if x is None or y is None:
        return None
    
    return y, x

def solicitar_posicion_pieza():
    p = input("\nIngrese la posición de la pieza que quiere seleccionar\n")
    resultado = posicion_valida(p)
    if not resultado:
        mensaje_validacion("posicion_fuera")
        return None
    return resultado

def validar_seleccion(pieza_selec, es_turno_blanco):
    if pieza_selec in CASILLAS_VACIAS:
        mensaje_validacion("casilla_vacia")
        return False
    piezas_aliadas = PIEZAS_BLANCAS if es_turno_blanco else PIEZAS_NEGRAS
    if pieza_selec not in piezas_aliadas:
        mensaje_validacion("turno_incorrecto")
        return False
    return True

def es_coordenada_valida(yn, xn):
    return 0 <= yn < 8 and 0 <= xn < 8