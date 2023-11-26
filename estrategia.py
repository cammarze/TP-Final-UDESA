def check_borde(x: int, y: int, z: int, diff: int = 0) -> tuple :
    """
    Chequea si los valores de (x, y, z) estan dentro de los limites del tablero. Si estan fuera,
    los ajusta de la siguiente manera:
    1) Reinicia los valores de (x, y) a los de la diagonal correspondiente. Cambia el valor de z para
    moverse a la misma diagonal pero "mas arriba".
    2) Cambia los valores de (x, y, z) para cambiar a la siguiente diagonal.

    Args:
        x (int): Valor del disparo en la coordenada x
        y (int): Valor del disparo en la coordenada y
        z (int): Valor del disparo en la coordenada z
        diff (int): Diferencia entre los valores de x e y

    Returns:
        x (int) --> Valor (actualizado) del disparo en la coordenada x
        y (int) --> Valor (actualizado) del disparo en la coordenada y
        z (int) --> Valor (actualizado) del disparo en la coordenada z

    """
    #Llego al borde del tablero, recorro la misma diagonal pero mas arriba
    if y < 0:
        x = 14
        y = x - diff
        z += 2
        #Me muevo a la siguiente diagonal
        if z > 9:
            x = 14
            y -= 2
            z = 0
    return x, y, z

def mov_diagonal(x: int, y, z, dx, dy, diff = 0):
    """
    """
    #Mientras mas grandes san dx y dy, mas distanciados estaran los disparos
    x -= dx
    y -= dy
    x, y, z = check_borde(x, y, z, diff)
    return x, y, z

def next_turn(coor_compu):
    coor_compu = coor_compu.split()
    compu_x = int(coor_compu[0])
    compu_y = int(coor_compu[1])
    compu_z = int(coor_compu[2])

    #Primera mitad
    if compu_x > compu_y:
        diff = compu_x - compu_y
        if diff in [2, 4, 6, 8, 10, 12]:
            compu_x, compu_y, compu_z = mov_diagonal(compu_x, compu_y, compu_z, 2, 2, diff)

        elif diff == 14:
            compu_z += 2
            if compu_z > 9:
                compu_x = 12
                compu_y = 14
                compu_z = 0
            else:
                compu_x, compu_y, compu_z = check_borde(compu_x, compu_y, compu_z, diff)

    #Segunda mitad
    elif compu_x < compu_y:
        diff = compu_y - compu_x
        if diff in [2, 4, 6, 8, 10, 12]:
            compu_y, compu_x, compu_z = mov_diagonal(compu_y, compu_x, compu_z, 2, 2, diff)

        elif diff == 14:
            compu_z += 2
            if compu_z > 9:
                compu_x = 14
                compu_y = 14
                compu_z = 0
            else:
                compu_y, compu_x, compu_z = check_borde(compu_y, compu_x, compu_z, diff)

    #Diagonal principal
    elif compu_x == compu_y:
        compu_x, compu_y, compu_z = mov_diagonal(compu_x, compu_y, compu_z, 2, 2)
        if compu_z > 9:
            compu_x = 14
            compu_y = 12
            compu_z = 0

    return f"{compu_x} {compu_y} {compu_z}"
