from constantes.piezas import BD, BT, BA, BC, ND, NT, NA, NC

def coronar_peon(es_turno_blanco):
    piezas_coronacion = f"d){BD}, t){BT}, a){BA}, c){BC}" if es_turno_blanco else f"d){ND}, t){NT}, a){NA}, c){NC}"
    print("\n¡Tu peón ha llegado al final del tablero!")
    
    selec_pieza_coronada = None
    while selec_pieza_coronada not in ['c', 'a', 't', 'd']:
        selec_pieza_coronada = input(f"Ingresa la pieza que deseas coronar\n{piezas_coronacion} ").lower()
    
    mapeo_piezas = {
        'c': BC if es_turno_blanco else NC,
        'a': BA if es_turno_blanco else NA,
        't': BT if es_turno_blanco else NT,
        'd': BD if es_turno_blanco else ND
    }
    
    return mapeo_piezas[selec_pieza_coronada]
