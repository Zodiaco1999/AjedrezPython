# Variables de las casillas del tablero
B = "◼ "   
N = "◻ "
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

PIEZAS_BLANCAS_SR = f"{BP}{BC}{BA}{BT}{BD}"
PIEZAS_NEGRAS_SR = f"{NP}{NC}{NA}{NT}{ND}"
PIEZAS_BLANCAS = f"{PIEZAS_BLANCAS_SR}{BR}"
PIEZAS_NEGRAS = f"{PIEZAS_NEGRAS_SR}{NR}"
TOTAL_PIEZAS = PIEZAS_BLANCAS + PIEZAS_NEGRAS
TOTAL_PIEZAS_SR = PIEZAS_BLANCAS_SR + PIEZAS_NEGRAS_SR
CASILLAS_VACIAS = {B, N}