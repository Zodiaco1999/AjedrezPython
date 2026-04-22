from constantes.piezas import BP, NP, BC, NC, BA, NA, BT, NT, BD, ND, BR, NR
from utilidades.buscador_piezas import hallar_posicion_pieza

def contar_piezas(tablero):
    piezas = {
        BP: 0, NP: 0,
        BC: 0, NC: 0,
        BA: 0, NA: 0,
        BT: 0, NT: 0,
        BD: 0, ND: 0,
        BR: 0, NR: 0
    }
    for fila in tablero:
        for pieza in fila:
            if pieza in piezas:
                piezas[pieza] += 1
    return piezas

def color_casilla_alfil(posicion):
    y, x = posicion
    if (y + x) % 2 == 0:
        return 'blanca'
    else:
        return 'oscura'

def hay_insuficiencia_material(tablero):
    """
    Verifica si hay insuficiencia de material para continuar la partida.
    Casos de insuficiencia:
    - Rey vs Rey
    - Rey + Caballo vs Rey
    - Rey + Alfil vs Rey
    - Rey + Alfil vs Rey + Alfil (del mismo color)
    """
    piezas = contar_piezas(tablero)
    
    # Contar piezas de ataque (no reyes)
    total_piezas_blancas_sr = (piezas[BP] + piezas[BC] + piezas[BA] + piezas[BT] + piezas[BD])
    total_piezas_negras_sr = (piezas[NP] + piezas[NC] + piezas[NA] + piezas[NT] + piezas[ND])
    
    # Caso 1: Rey vs Rey
    if total_piezas_blancas_sr == 0 and total_piezas_negras_sr == 0:
        return True
    
    # Caso 2: Rey + Caballo vs Rey
    if ((piezas[BC] == 1 and piezas[BD] == 0 and piezas[BA] == 0 and 
         piezas[BT] == 0 and piezas[BP] == 0 and total_piezas_negras_sr == 0) 
        or
        (piezas[NC] == 1 and piezas[ND] == 0 and piezas[NA] == 0 and 
         piezas[NT] == 0 and piezas[NP] == 0 and total_piezas_blancas_sr == 0)):
        return True
    
    # Caso 3: Rey + Alfil vs Rey
    if ((piezas[BA] == 1 and piezas[BC] == 0 and piezas[BD] == 0 and 
         piezas[BT] == 0 and piezas[BP] == 0 and total_piezas_negras_sr == 0) 
        or
        (piezas[NA] == 1 and piezas[NC] == 0 and piezas[ND] == 0 and 
         piezas[NT] == 0 and piezas[NP] == 0 and total_piezas_blancas_sr == 0)):
        return True
    
    # Caso 4: Rey + Alfil vs Rey + Alfil (del mismo color)
    if (piezas[BA] == 1 and piezas[NA] == 1 and
        piezas[BC] == 0 and piezas[NC] == 0 and
        piezas[BD] == 0 and piezas[ND] == 0 and
        piezas[BT] == 0 and piezas[NT] == 0 and
        piezas[BP] == 0 and piezas[NP] == 0):
        
        # Verificar que los alfiles están en casillas del mismo color
        pos_alfil_blanco = hallar_posicion_pieza(tablero, BA)
        pos_alfil_negro = hallar_posicion_pieza(tablero, NA)
        if pos_alfil_blanco and pos_alfil_negro:
            color_blanco = color_casilla_alfil(pos_alfil_blanco)
            color_negro = color_casilla_alfil(pos_alfil_negro)
            if color_blanco == color_negro:
                return True
    
    return False