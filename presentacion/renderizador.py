def nomenclatura_columnas():
    print("    A     B     C     D     E     F     G     H")   
       
def imprimir_tablero(tablero):
    print()
    nomenclatura_columnas()
    for i in range(8):
        print(8 - i, tablero[i][:], 8 - i)
    nomenclatura_columnas()