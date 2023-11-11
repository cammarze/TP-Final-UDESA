import matplotlib.pyplot as plt
import numpy as np
import math


def preguntar_coordenadas(prompt: str, prompt_fallido: str,tamaño : tuple = (0,0,0)):
    coordenada = input(prompt)
    while len(coordenada.split()) != 3 or not chequear_coordenadas(coordenada, tamaño[0], tamaño[1], tamaño[2]):
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

class Vehiculo:
    def __init__(self, nombre, vida, cantidad, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.cantidad = cantidad
        self.contador = 0 #inicializo en 0
        self.tamaño = tamaño
        self.x, self.y, self.z = np.indices((15, 15, 10))
        self.rotacion = 0 #inicializar en 0

    def ColocarVehiclo(self):
        self.contador += 1  #incrementa el contador al colocar el vehiculo
        Text_coor = self.RotarVehiculo()
        return preguntar_coordenadas(f"Jugador 1, ingrese las coordenadas de {self.nombre} {self.contador} {Text_coor}: ",
                                     f"Datos invalidos\nIngrese el nucleo de {self.nombre} {self.contador} (x y z): ",
                                     self.tamaño)
    def RotarVehiculo(self):
        num_rot = int(input(f"Ingrese la cantidad de veces que quiere rotar el {self.nombre} {self.contador}: "))
        self.rotacion = 90*num_rot%360
        return "(x y z)" if self.rotacion == 0 or self.rotacion == 180 else "(y x z)"

    def RecibirGolpe(self):
        pass
    
class Globo(Vehiculo):
    def __init__(self):
        super().__init__(nombre="globo",vida=1, cantidad=5, tamaño=(3, 3, 3))
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        globo_pltshow = (
        (self.x >= (Coor_x - 1)) & (self.x < (Coor_x + 2)) &
        (self.y >= (Coor_y - 1)) & (self.y < (Coor_y + 2)) &
        (self.z >= (Coor_z - 1)) & (self.z < (Coor_z + 2))
        )
        return globo_pltshow
    def RecibirGolpe(self):
        return self.vida -1

class Zeppelin(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="zeppelin",vida = 3, cantidad = 2, tamaño = (5,2,2) )
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        if self.rotacion == 0 or self.rotacion == 180:
            zeppelin_pltshow = (
        (self.x >= (Coor_x - 2)) & (self.x < (Coor_x + 3)) &
        (self.y >= Coor_y) & (self.y < (Coor_y + 2)) &
        (self.z >= (Coor_z)) & (self.z < (Coor_z + 2))
        )
        else:
            zeppelin_pltshow = (
        (self.y >= (Coor_x - 2)) & (self.y < (Coor_x + 3)) &
        (self.x >= Coor_y) & (self.x < (Coor_y + 2)) &
        (self.z >= (Coor_z)) & (self.z < (Coor_z + 2))
        )            
        return zeppelin_pltshow
    def RecibirGolpe(self):
        return self.vida -1

class Avion(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="avion",vida= 2, cantidad = 3, tamaño = (4,3,2))
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        if self.rotacion == 0:
            avion_pltshow = (
        (self.x >= (Coor_x - 1)) & (self.x < (Coor_x + 3)) &
        (self.y == Coor_y) & (self.z == Coor_z) |
        (self.x == Coor_x + 1) & (self.y >= (Coor_y - 1)) & (self.y < (Coor_y + 2)) & (self.z == Coor_z) |
        (self.x == (Coor_x - 1)) & (self.y == Coor_y) & (self.z == (Coor_z + 1))
        )
        elif self.rotacion == 90:
            avion_pltshow = (
        (self.y >= (Coor_x - 1)) & (self.y < (Coor_x + 3)) &
        (self.x == Coor_y) & (self.z == Coor_z) |
        (self.y == Coor_x + 1) & (self.x >= (Coor_y - 1)) & (self.x < (Coor_y + 2)) & (self.z == Coor_z) |
        (self.y == (Coor_x - 1)) & (self.x == Coor_y) & (self.z == (Coor_z + 1))
        )
        elif self.rotacion == 180:
            avion_pltshow = (
        (self.x >= (Coor_x - 1)) & (self.x < (Coor_x + 3)) &
        (self.y == Coor_y) & (self.z == Coor_z) |
        (self.x == Coor_x ) & (self.y >= (Coor_y - 1)) & (self.y < (Coor_y + 2)) & (self.z == Coor_z) |
        (self.x == (Coor_x + 2)) & (self.y == Coor_y) & (self.z == (Coor_z + 1))
        )
        else:
            avion_pltshow = (
        (self.y >= (Coor_x - 1)) & (self.y < (Coor_x + 3)) &
        (self.x == Coor_y) & (self.z == Coor_z) |
        (self.y == Coor_x) & (self.x >= (Coor_y - 1)) & (self.x < (Coor_y + 2)) & (self.z == Coor_z) |
        (self.y == (Coor_x + 2)) & (self.x == Coor_y) & (self.z == (Coor_z + 1))
        )
            

        return avion_pltshow
    def RecibirGolpe(self):
        return self.vida -1

class ElevadorEspacial(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="elevador espacial",vida=4, cantidad = 1, tamaño =(1,1,10)) #El tamaño en realidad es 10, pero 
        self.orientation = 0

    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        elevevador_espacial_pltshow = (
        (self.x == Coor_x) & (self.y == Coor_y) & (self.z < 10)
        )
        return elevevador_espacial_pltshow
    def RecibirGolpe(self):
        return self.vida -1
class Tablero:
    def __init__(self, dim_x, dim_y, dim_z):

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z

        self.tablero = np.zeros((dim_x, dim_y, dim_z))
        self.tablero_disparos = np.full((dim_x, dim_y, dim_z), '?', dtype=str)

x,y,z = np.indices((15, 15, 10))
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig.set_size_inches(6, 6)

Juan = Avion()
Colocar = Juan.ColocarVehiclo()

ax.voxels(Colocar,color="purple" ,edgecolor='k')

plt.show()
