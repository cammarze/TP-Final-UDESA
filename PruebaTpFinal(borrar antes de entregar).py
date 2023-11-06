import matplotlib.pyplot as plt
import numpy as np


def preguntar_coordenadas(prompt: str, prompt_fallido: str,tamaño : tuple = (0,0,0)):
    coordenada = input(prompt)
    while len(coordenada.split()) != 3 or not chequear_coordenadas(coordenada, tamaño[0], tamaño[1], tamaño[2]):
        coordenada = input(prompt_fallido)
    return coordenada

def chequear_coordenadas(texto_num:str, tamaño_x: int = 0, tamaño_y: int = 0, tamaño_z: int = 0) -> bool:
    lista_num = texto_num.split()
    Chequeo = 0

    for elemento in lista_num:
        if not elemento.isdecimal():
            return False
    if (0 + tamaño_x//2 - 1) <= int(lista_num[0]) < (15 - tamaño_x//2):
        Chequeo += 1
    if (0 + tamaño_y//2 - 1) <= int(lista_num[1]) < (15 - tamaño_y//2):
        Chequeo += 1
    if (0 + tamaño_z//2 - 1) <= int(lista_num[2]) < (10 - tamaño_z//2):
        Chequeo += 1
    if Chequeo == len(lista_num):
        return True
    else: 
        return False
class Vehiculo:
    def _init_(self, nombre, vida, cantidad, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.cantidad = cantidad
        self.contador = self.cantidad - 1
        self.tamaño = tamaño
        self.x, self.y, self.z = np.indices((15, 15, 10))

    def ColocarVehiclo(self):
        self.cantidad -= 1
        Nucleo = preguntar_coordenadas(f"Ingrese el nucleo de {self.nombre} {self.contador - self.cantidad} (x y z): ",f"Datos invalidos\nIngrese el nucleo de {self.nombre} {self.contador - self.cantidad} (x y z): ",self.tamaño)
        return map(int,Nucleo.split())
    def RotarVehiculo(self):
        pass
    def RecibirGolpe(self):
        pass

    
class Globo(Vehiculo):
    def __init__(self):
        super()._init_(nombre="globo",vida=1, cantidad=5, tamaño=(3, 3, 3))
    
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
    def RotarVehiculo(self):
        pass

class Zeppelin(Vehiculo):
    def __init__(self) -> None:
        super()._init_(nombre="zeppelin",vida = 3, cantidad = 2, tamaño = (5,2,2) )
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        zeppelin_pltshow = (
        (self.x >= (Coor_x - 2)) & (self.x < (Coor_x + 3)) &
        (self.y >= Coor_y) & (self.y < (Coor_y + 2)) &
        (self.z >= (Coor_z)) & (self.z < (Coor_z + 2))
        )
        return zeppelin_pltshow
    def RecibirGolpe(self):
        return self.vida -1
    def RotarVehiculo(self):
        pass


class Avion(Vehiculo):
    def __init__(self) -> None:
        super()._init_(nombre="avion",vida= 2, cantidad = 3, tamaño = (4,3,2))
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        avion_pltshow = (
        (self.x >= (Coor_x - 1)) & (self.x < (Coor_x + 3)) &
        (self.y == Coor_y) & (self.z == Coor_z) |
        (self.x == Coor_x + 1) & (self.y >= (Coor_y - 1)) & (self.y < (Coor_y + 2)) & (self.z == Coor_z) |
        (self.x == (Coor_x - 1)) & (self.y == Coor_y) & (self.z == (Coor_z + 1))

        )
        return avion_pltshow
    def RecibirGolpe(self):
        return self.vida -1
    def RotarVehiculo(self):
        pass

class ElevadorEspacial(Vehiculo):
    def __init__(self) -> None:
        super()._init_(nombre="elevador espacial",vida=4, cantidad = 1, tamaño =(1,1,0)) #El tamaño en realidad es 10, pero 
    
    def ColocarVehiclo(self):
        Coor_x, Coor_y, Coor_z = super().ColocarVehiclo()
        elevevador_espacial_pltshow = (
        (self.x == Coor_x) & (self.y == Coor_y) & (self.z < 10)
        )
        return elevevador_espacial_pltshow
    def RecibirGolpe(self):
        return self.vida -1
    def RotarVehiculo(self):
        pass



fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
fig.set_size_inches(6, 6)

Juan = Zeppelin()
Colocar = Juan.ColocarVehiclo()
ax.voxels(Colocar,color="r" ,edgecolor='k')

plt.show()