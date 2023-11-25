import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import numpy as np
import math
import random

import codigo_entero as c

def next_turn(coor_compu):
    coor_compu = coor_compu.split()
    compu_x = int(coor_compu[0])
    compu_y = int(coor_compu[1])
    compu_z = int(coor_compu[2])

    if compu_x == compu_y:
        compu_x = 16
        compu_y = 14
    
    #Primera mitad
    if compu_x > compu_y:
        if (compu_x - compu_y) == 2: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0: #Llego al borde del tablero
                compu_x = 16
                compu_y = 14
                compu_z += 2
                if compu_z == 10: #Paso a la siguiente diagonal
                    compu_x = 16
                    compu_y = 12
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu

        if (compu_x - compu_y) == 4: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0:
                compu_x = 16
                compu_y = 12
                compu_z += 2
                if compu_z == 10:
                    compu_x = 16
                    compu_y = 10
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_x - compu_y) == 6: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0:
                compu_x = 16
                compu_y = 10
                compu_z += 2
                if compu_z == 10:
                    compu_x = 16
                    compu_y = 8
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_x - compu_y) == 8: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0:
                compu_x = 16
                compu_y = 8
                compu_z += 2
                if compu_z == 10:
                    compu_x = 16
                    compu_y = 6
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_x - compu_y) == 10: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0:
                compu_x = 16
                compu_y = 6
                compu_z += 2
                if compu_z == 10:
                    compu_x = 16
                    compu_y = 4
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_x - compu_y) == 12: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_y < 0:
                compu_x = 16
                compu_y = 4
                compu_z += 2
                if compu_z == 10:
                    compu_x = 14
                    compu_y = 0
                    compu_z = 10
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
                
        #Esquina
        if (compu_x - compu_y) == 14:
            compu_z -= 2
            if compu_z < 0: #Comienzo a recorrer otra mitad
                compu_x = 14
                compu_y = 16
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu


    #Segunda mitad           
    if compu_x < compu_y:
        if (compu_y - compu_x) == 2: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0: #Llego al borde del tablero
                compu_x = 14
                compu_y = 16
                compu_z += 2
                if compu_z == 10: #Paso a la siguiente diagonal
                    compu_x = 12
                    compu_y = 16
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu

        if (compu_y - compu_x) == 4: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0:
                compu_x = 12
                compu_y = 16
                compu_z += 2
                if compu_z == 10:
                    compu_x = 10
                    compu_y = 16
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_y - compu_x) == 6: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0:
                compu_x = 10
                compu_y = 16
                compu_z += 2
                if compu_z == 10:
                    compu_x = 8
                    compu_y = 16
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_y - compu_x) == 8: #Diagonal
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0:
                compu_x = 8
                compu_y = 16
                compu_z += 2
                if compu_z == 10:
                    compu_x = 6
                    compu_y = 16
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_y - compu_x) == 10:
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0:
                compu_x = 6
                compu_y = 16
                compu_z += 2
                if compu_z == 10:
                    compu_x = 4
                    compu_y = 16
                    compu_z = 0
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        if (compu_y - compu_x) == 12:
            compu_x -= 2
            compu_y -= 2
            if compu_x < 0:
                compu_x = 4
                compu_y = 16
                compu_z += 2
                if compu_z == 10:
                    compu_x = 0
                    compu_y = 14
                    compu_z = 10
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
            
        #Esquina
        if (compu_y - compu_x) == 14:
            compu_z -= 2
            if compu_z < 0: #Comienzo a recorrer otra mitad
                pass
            else:
                coor_compu = f"{compu_x} {compu_y} {compu_z}"
                return coor_compu
