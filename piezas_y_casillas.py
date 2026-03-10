# Variables de las casillas del tablero
N = "◼ "   
B = "◻ "
# Variables de piezas blancas
BP = "♟ "
BC = "♞ "
BA = "♝ "
BT = "♜ "
BR = "♚ "
BD = "♛ "
# Variables de piezas negras
NP = "♙ " 
NC = "♘ "
NA = "♗ "
NT = "♖ "
NR = "♔ "
ND = "♕ "

piezas_blancas_sr = f"{BP}{BC}{BA}{BT}{BD}"
piezas_negras_sr = f"{NP}{NC}{NA}{NT}{ND}"
piezas_blancas = f"{piezas_blancas_sr}{BR}"
piezas_negras = f"{piezas_negras_sr}{NR}"

all_piezas = piezas_blancas + piezas_negras