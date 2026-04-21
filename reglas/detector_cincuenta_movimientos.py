from constantes.piezas import BP, NP

contador_cincuenta = 0

def reiniciar_contador():
    global contador_cincuenta
    contador_cincuenta = 0

def incrementar_contador():
    global contador_cincuenta
    contador_cincuenta += 1

def hay_cincuenta_movimientos():
    return contador_cincuenta >= 50

def verificar_movimiento(pieza_selec, captura_realizada):
    """
    Verifica si el movimiento es de peón o captura.
    Si lo es, reinicia el contador.
    Si no lo es, incrementa el contador.
    
    Args:
        pieza_selec: pieza que se movió
        captura_realizada: bool indicando si hubo captura
    """
    if captura_realizada or pieza_selec in {BP, NP}:
        reiniciar_contador()
    else:
        incrementar_contador()
