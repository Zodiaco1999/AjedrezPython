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