MENSAJES_ERROR = {
    "posicion_fuera": "¡La posición ingresada está fuera del tablero!",
    "casilla_vacia": "¡No ha seleccionado ninguna pieza!",
    "turno_incorrecto": "¡Esa pieza no pertenece a tu color!",
    "movimiento_ilegal": "¡Esa pieza no puede moverse así!",
    "rey_en_jaque": "¡Movimiento ilegal! Tu rey estaría en jaque.",
    "posicion_invalida": "¡Posición inválida!"
}

def mensaje_validacion(clave):
    mensaje = MENSAJES_ERROR.get(clave, "Error desconocido en la validación.")
    print(f"\n{mensaje}\n")
    input("Presione Enter para continuar...")

def mensaje_pieza(es_simulacion, mensaje):
    if not es_simulacion:
        print(f"\n{mensaje}")