from diccionarios.mapeos import columnas_a_indices, filas_a_indices

def posicion_valida(p):
    if len(p) != 2:
        return False
    
    p = p.lower() 
    
    x = columnas_a_indices.get(p[0])
    y = filas_a_indices.get(p[1])
    
    if x is None or y is None:
        return None
    
    return y, x

def es_coordenada_valida(yn, xn):
    return 0 <= yn < 8 and 0 <= xn < 8