import matplotlib.pyplot as plt
import numpy as np
import math


def chequear_solapamiento(vehiculo, nucleo, espacio):
    if type(vehiculo) == Globo:
        pass
    return np.all(espacio[nucleo[0]-1:nucleo[0]+2,nucleo[1]-1:nucleo[1]+2,nucleo[2]-1:nucleo[2]+2]<0)




def preguntar_coordenadas(prompt: str, prompt_fallido: str,tamaño : tuple = (0,0,0)):
    coordenada = input(prompt)
    while len(coordenada.split()) != 3 or not chequear_coordenadas(coordenada, *tamaño):
        coordenada = input(prompt_fallido)
    return map(int,coordenada.split())

def chequear_coordenadas(texto_num:str, tamaño_x: int = 0, tamaño_y: int = 0, tamaño_z: int = 0) -> bool:
    lista_num = texto_num.split()
    Chequeo = 0

    for elemento in lista_num:
        if not elemento.isdecimal():
            return False
    Chequeo_x = math.ceil(tamaño_x/2 - 1) if tamaño_x > 0 else 0
    Chequeo_y = math.ceil(tamaño_y/2 - 1) if tamaño_y > 0 else 0
    Chequeo_z = math.ceil(tamaño_z/2 - 1) if tamaño_z > 0 else 0
    if Chequeo_x <= int(lista_num[0]) < (15 - tamaño_x//2):
        Chequeo += 1
    if Chequeo_y <= int(lista_num[1]) < (15 - tamaño_y//2):
        Chequeo += 1
    if Chequeo_z <= int(lista_num[2]) < (10 - tamaño_z//2) or tamaño_z == 10:
        Chequeo += 1
    if Chequeo == len(lista_num):
        return True
    else: 
        return False
    

class Tablero:
    def __init__(self, dim_x=15, dim_y=15, dim_z=10):

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z

        self.tablero = np.zeros((dim_x, dim_y, dim_z))

    def check_solapa(self,vehiculo, nuc_x,nuc_y,nuc_z):
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x
        
        if type(vehiculo) == Globo:
            check_x1, check_y1, check_z1 = -1, -1, -1
            check_x2, check_y2, check_z2 = 2, 2, 2
        elif type(vehiculo) == Zeppelin:
            check_x1, check_y1, check_z1 = -2, 0, 0
            check_x2, check_y2, check_z2 = 3, 2, 2
            if vehiculo.rotacion in [90,270]:
                check_x1, check_y1 = check_y1, check_x1
                check_x2, check_y2 = check_y2, check_x2
        elif type(vehiculo) == Avion:
            check_x1, check_x2, check_x3, check_x4, check_x5, check_x6 = -1, 3, 1, 2,-1,0
            check_y1, check_y2, check_y3, check_y4, check_y5, check_y6 = 0, 1, -1, 2,1,1
            if vehiculo.rotacion in [90,270]:
                check_x1, check_y1 = check_y1, check_x1
                check_x2, check_y2 = check_y2, check_x2
                check_x3, check_y3 = check_y3, check_x3
                check_x4, check_y4 = check_y4, check_x4
                check_x5, check_y5 = check_y5, check_x5
                check_x6, check_y6 = check_y6, check_x6
                if vehiculo.rotacion == 270:
                    check_x3, check_x4, check_x5, check_x6 = 1,2,2, 3
            elif vehiculo.rotacion == 180:
                check_x3, check_x4, check_x5, check_x6 = 0, 1, 2, 3
                return np.all(self.tablero[nuc_x + check_x1 : nuc_x + check_x2, nuc_y + check_y1 : nuc_y + check_y2, nuc_z : nuc_z + 1]<=0) and np.all(self.tablero[nuc_x + check_x3 : nuc_x + check_x4, nuc_y + check_y3 : nuc_y + check_y4, nuc_z : nuc_z + 1]<=0) and np.all(self.tablero[nuc_x + check_x5 : nuc_x + check_x6, nuc_y + check_y5 : nuc_y + check_y6, nuc_z + 1  : nuc_z + 2]<=0)
        else:    
            return np.all(self.tablero[nuc_x  : nuc_x + 1 , nuc_y : nuc_y + 1 , 0 : 10]<=0)
        return np.all(self.tablero[nuc_x + check_x1: nuc_x + check_x2, nuc_y + check_y1 : nuc_y + check_y2, nuc_z + check_z1 : nuc_z + check_z2]<=0)






    def RotarVehiculo(self, vehiculo):
        if type(vehiculo) in [Avion, Zeppelin]:
            num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
            while not num_rot.strip().isdecimal():
                num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
            num_rot = int(num_rot)
            vehiculo.rotacion = 90*num_rot%360


    def colocar_Vehiculo(self, vehiculo):
        self.RotarVehiculo(vehiculo)
        textcoor = "(x y z)" if vehiculo.rotacion in [0,180] else "(y x z)"
        nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador} {textcoor}: ",
                                     f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador} {textcoor}: ",
                                     vehiculo.tamaño)
        while not self.check_solapa(vehiculo, nuc_x, nuc_y, nuc_z):
            print("Solapamiento entre vehiculos. Ingrese otra vez")
            nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador} {textcoor}: ", 
                                                        f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador} {textcoor}: ",
                                                        vehiculo.tamaño)
        if type(vehiculo) == Globo:
            self.tablero[nuc_x - 1: nuc_x + 2, nuc_y - 1: nuc_y + 2, nuc_z -1: nuc_z + 2] = 1
        if type(vehiculo) == Zeppelin:
            if vehiculo.rotacion in [0,180]:
                self.tablero[nuc_x - 2: nuc_x + 3, nuc_y: nuc_y + 2, nuc_z : nuc_z + 2] = 1
            else:
                nuc_x, nuc_y = nuc_y, nuc_x
                self.tablero[nuc_x: nuc_x + 2, nuc_y - 2: nuc_y + 3, nuc_z : nuc_z + 2] = 1
        if type(vehiculo) == Avion:
            pass
        if type(vehiculo) == ElevadorEspacial:
            self.tablero[nuc_x:nuc_x + 1, nuc_y: nuc_y + 1, 0 : 10] = 1 
        vehiculo.contador += 1
    
    
    
    
    def mostrar_Tablero(self):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig.set_size_inches(6, 6)
        ax.voxels(self.tablero, color="purple", edgecolor='k')
        plt.show()


class Vehiculo:
    def __init__(self, nombre, vida, cantidad, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.cantidad = cantidad
        self.contador = 0
        self.tamaño = tamaño
        self.rotacion = 0


    
class Globo(Vehiculo):
    def __init__(self):
        super().__init__(nombre="globo",vida=1, cantidad=5, tamaño=(3, 3, 3))
    


class Zeppelin(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="zeppelin",vida = 3, cantidad = 2, tamaño = (5,2,2) )
    




class Avion(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="avion",vida= 2, cantidad = 3, tamaño = (4,3,2))
    

class ElevadorEspacial(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="elevador espacial",vida=4, cantidad = 1, tamaño =(1,1,10)) #El tamaño en realidad es 10, pero 





tablero = Tablero()
vehiculos = [Globo, Zeppelin, ElevadorEspacial]
for vehiculo in vehiculos:
    vehic = vehiculo()
    for i in range(vehic.cantidad):  #iterar en base a la cantidad de cada vehiculo
        tablero.colocar_Vehiculo(vehic)
        tablero.mostrar_Tablero()
        



