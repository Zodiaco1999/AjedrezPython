# Diccionario central de mensajes
MENSAJES_ERROR = {
    "posicion_fuera": "¡La posición ingresada está fuera del tablero!",
    "casilla_vacia": "¡No ha seleccionado ninguna pieza!",
    "turno_incorrecto": "¡Esa pieza no pertenece a tu color!",
    "movimiento_ilegal": "¡Esa pieza no puede moverse así!",
    "rey_en_jaque": "¡Movimiento ilegal! Tu rey estaria en jaque.",
    "posicion_invalida": "¡Posición invalida!"
}

estado_enroque = {
    'blanco': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': '♜ ', 
        'rey_rival': '♔ '
    },
    'negro': {
        'rey_movido': False, 
        'torre_der_movida': False, 
        'torre_izq_movida': False, 
        'torre': '♖ ', 
        'rey_rival': '♚ '
    }
}

def mensaje_validacion(clave):
    """Muestra el error correspondiente y pausa la ejecución."""
    mensaje = MENSAJES_ERROR.get(clave, "Error desconocido en la validación.")
    print(f"\n{mensaje}\n")
    input("Presione Enter para continuar...")