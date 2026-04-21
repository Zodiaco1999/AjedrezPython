from constantes.piezas import BP, NP, BT, NT, BR, NR, PIEZAS_NEGRAS_SR, PIEZAS_BLANCAS_SR
from contextlib import contextmanager
import copy

estado_enroque = {
    'blanco': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': BT, 
        'rey_rival': NR
    },
    'negro': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': NT, 
        'rey_rival': BR
    }
}

config_peon = {
    'blanco': {'dir': -1, 'inicio': 6, 'paso': 3, 'rival_peon': NP, 'rivales': PIEZAS_NEGRAS_SR, 'rival_color': 'negro', 'coronacion': 0},
    'negro': {'dir': 1, 'inicio': 1, 'paso': 4, 'rival_peon': BP, 'rivales': PIEZAS_BLANCAS_SR, 'rival_color': 'blanco', 'coronacion': 7}
}

estado_peones = {
    'blanco': {'salto_doble': False , 'columna': None},
    'negro': {'salto_doble': False, 'columna': None}
}

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