from estado.estados_piezas import estado_peones
    
def turnos(t):
    es_turno_blanco = t % 2 != 0
    color = "blanco" if es_turno_blanco else "negro"
    estado_peones[color]['salto_doble'] = False
    estado_peones[color]['columna'] = None
    
    print(f"\n================Turno de las {'blancas' if es_turno_blanco else 'negras'}================")
    return es_turno_blanco