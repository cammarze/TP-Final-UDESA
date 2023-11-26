import random
import math

def preguntar_coordenadas(prompt: str, prompt_fallido: str, jugador : str,tamaño : tuple = (0,0,0),):
    """
    Pregunta al jugador coordenadas (x,y,z) para la ubicacion de vehiculos dentro del tablero
    Args:
    - prompt (str): Mensaje para la solicitud de coordenadas (x,y,z)
    - prompt_fallido (str): Mensaje de error para coordenadas invalidas
    - jugador (str) : Se identifica al jugador
    - tamano (tuple) : Tamano del tablero. Por default es (0,0,0)
    
    Returns:
    - tuple --> Tupla de ints que representan las coordenadas validas ingresadas por el usuario ("jugador1") o generadas automaticamente para el jugador 2
    """
    if jugador == "Jugador1":
        coordenada = input(prompt)
        while len(coordenada.split()) != 3 or not chequear_coordenadas(coordenada, *tamaño):
            coordenada = input(prompt_fallido)
    else:
        coordenada = f"{random.randint(0,14)} {random.randint(0,14)} {random.randint(0,9)}"
        while not chequear_coordenadas(coordenada,*tamaño):
            coordenada = f"{random.randint(0,14)} {random.randint(0,14)} {random.randint(0,9)}"
    return map(int,coordenada.split())


def chequear_coordenadas(texto_num:str, tamaño_x: int = 0, tamaño_y: int = 0, tamaño_z: int = 0) -> bool:
    """
    Chequea si las coordenadas estan dentro de los limites del tamano del tablero.
    Args:
    - texto_num (str): Las coordenadas en formato de texto
    - tamaño_x (int): Tamano del tablero en el eje X. Por default es 0
    - tamaño_y (int): Tamano del tablero en el eje Y. Por default es 0
    - tamano_z (int): Tamano del tablero en el eje Z. Por default es 0

    Returns:
    - bool --> Retornea True en caso de que las coordenadas estan dentro de los limitess del tablero. Flse caso contrario. 
    """
    lista_coor = texto_num.split()
    Chequeo = 0

    for elemento in lista_coor:
        if not elemento.isdecimal():
            return False
    Chequeo_x = math.ceil(tamaño_x/2 - 1) if tamaño_x > 0 else 0
    Chequeo_y = math.ceil(tamaño_y/2 - 1) if tamaño_y > 0 else 0
    Chequeo_z = math.ceil(tamaño_z/2 - 1) if tamaño_z > 0 else 0
    if Chequeo_x <= int(lista_coor[0]) < (15 - tamaño_x//2):
        Chequeo += 1
    if Chequeo_y <= int(lista_coor[1]) < (15 - tamaño_y//2):
        Chequeo += 1
    if Chequeo_z <= int(lista_coor[2]) < (10 - tamaño_z//2) or (tamaño_z == 10 and 0 <= int(lista_coor[2]) < 10):
        Chequeo += 1
    if Chequeo == len(lista_coor):
        return True
    else: 
        return False