import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import numpy as np
import math
import random 





def preguntar_coordenadas(prompt: str, prompt_fallido: str, jugador,tamaño : tuple = (0,0,0),):
    if jugador == "Jugador1":
        coordenada = input(prompt)
        while len(coordenada.split()) != 3 or not chequear_coordenadas(coordenada, *tamaño):
            coordenada = input(prompt_fallido)
    else:
        coordenada = f"{random.randint(0,14)} {random.randint(0,14)} {random.randint(0,9)}"
        while not chequear_coordenadas(coordenada, *tamaño):
            coordenada = f"{random.randint(0,14)} {random.randint(0,14)} {random.randint(0,9)}"
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
            return np.all(self.tablero[nuc_x - 1 : nuc_x + 2 , nuc_y - 1 : nuc_y + 2 , nuc_z - 1:nuc_z + 2]<=0)
       
        elif type(vehiculo) == Zeppelin:
            check_x = [-2,3]
            check_y = [0,2]
            if vehiculo.rotacion in [90,270]:
                check_x, check_y = check_y, check_x
            return np.all(self.tablero[nuc_x + check_x[0] : nuc_x + check_x[1] , nuc_y + check_y[0] : nuc_y + check_y[1] , nuc_z : nuc_z + 2]<=0)
       
        elif type(vehiculo) == Avion:
            if vehiculo.rotacion in [0,90]:
                    check_1 = 1
                    check_2 = -1
            else:
                    check_1 = 0
                    check_2 = 2
            if vehiculo.rotacion in [0,180]: 
                return (np.all(self.tablero[nuc_x - 1 : nuc_x + 3 , nuc_y, nuc_z]<=0) and 
                np.all(self.tablero[nuc_x + check_1, nuc_y - 1 : nuc_y + 2 , nuc_z]<=0) and 
                np.all(self.tablero[nuc_x + check_2, nuc_y, nuc_z + 1]<=0))
            else:
                return (np.all(self.tablero[ nuc_x, nuc_y -1 : nuc_y + 3  , nuc_z]<=0) and 
                np.all(self.tablero[nuc_x - 1 : nuc_x + 2  , nuc_y + check_1, nuc_z]<=0) and 
                np.all(self.tablero[nuc_x, nuc_y + check_2, nuc_z + 1]<=0))
        else:    
            return np.all(self.tablero[nuc_x, nuc_y, 0 : 10]<=0)



    def RotarVehiculo(self, vehiculo, jugador):
        if type(vehiculo) in [Avion, Zeppelin]:
            if jugador == "Jugador1":
                num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
                while not num_rot.strip().isdecimal():
                    num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
                num_rot = int(num_rot)
            else:
                num_rot = random.randint(0,25)
            vehiculo.rotacion = 90*num_rot%360


    def colocar_Vehiculo(self, vehiculo, jugador):
        self.RotarVehiculo(vehiculo, jugador)
        textcoor = "(x y z)" if vehiculo.rotacion in [0,180] else "(y x z)"
        nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador} {textcoor}: ",
                                     f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador} {textcoor}: ",jugador,
                                     vehiculo.tamaño)
        
        while not self.check_solapa(vehiculo, nuc_x, nuc_y, nuc_z):
            if jugador == "Jugador1":
                print("Solapamiento entre vehiculos. Ingrese otra vez")
            nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador} {textcoor}: ", 
                                                        f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador} {textcoor}: ",jugador,
                                                        vehiculo.tamaño)
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x
        if type(vehiculo) == Globo:
            self.tablero[nuc_x - 1: nuc_x + 2, nuc_y - 1: nuc_y + 2, nuc_z -1: nuc_z + 2] = 1 + type(vehiculo).contador/10
        elif type(vehiculo) == Zeppelin:
            if vehiculo.rotacion in [0,180]:
                self.tablero[nuc_x - 2: nuc_x + 3, nuc_y: nuc_y + 2, nuc_z : nuc_z + 2] = 2 + type(vehiculo).contador/10
            else:
                self.tablero[nuc_x: nuc_x + 2, nuc_y - 2: nuc_y + 3, nuc_z : nuc_z + 2] = 2 + type(vehiculo).contador/10
        elif type(vehiculo) == Avion:
            if vehiculo.rotacion in [0,90]:
                    suma_1 = 1
                    suma_2 = -1
            else:
                    suma_1 = 0
                    suma_2 = 2
            if vehiculo.rotacion in [0,180]:
                self.tablero[nuc_x - 1 : nuc_x + 3 , nuc_y, nuc_z] = 3 + type(vehiculo).contador/10
                self.tablero[nuc_x + suma_1 , nuc_y - 1 : nuc_y + 2 , nuc_z] = 3 + type(vehiculo).contador/10
                self.tablero[nuc_x + suma_2 , nuc_y, nuc_z + 1] = 3 + type(vehiculo).contador/10
            else:
                self.tablero[nuc_x, nuc_y - 1 : nuc_y + 3, nuc_z] = 3 + type(vehiculo).contador/10
                self.tablero[nuc_x - 1 : nuc_x + 2, nuc_y + suma_1, nuc_z] = 3 + type(vehiculo).contador/10
                self.tablero[nuc_x, nuc_y + suma_2, nuc_z + 1] = 3 + type(vehiculo).contador/10
        else:
            self.tablero[nuc_x, nuc_y, 0 : 10] = 4 
        type(vehiculo).contador += 1
      
    def agregar_colores(self):
        tablero_plt = np.copy(self.tablero).astype(int)
        colores = np.zeros(self.tablero.shape + (4,), dtype=np.float32)
        colores[tablero_plt == 1] = plt_colors.to_rgba("darkred", alpha=0.7)
        colores[tablero_plt == 2] = plt_colors.to_rgba("midnightblue", alpha=0.7)
        colores[tablero_plt == 3] = plt_colors.to_rgba("lightgray", alpha=0.7) 
        colores[tablero_plt == 4] = plt_colors.to_rgba("darkslategray", alpha=0.7)
        return colores
    
    def mostrar_Tablero(self):
        colores = self.agregar_colores()
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        fig.set_size_inches(6, 6)
        ax.voxels(self.tablero, facecolors=colores , edgecolor='k')
        plt.show()


class Vehiculo:
    def __init__(self, nombre, vida, cantidad, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.cantidad = cantidad
        self.tamaño = tamaño
        self.rotacion = 0
        dict_datos = {}


    
class Globo(Vehiculo):
    def __init__(self):
        super().__init__(nombre="globo",vida=1, cantidad=5, tamaño=(3, 3, 3))
    contador = 1
    


class Zeppelin(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="zeppelin",vida = 3, cantidad = 2, tamaño = (5,2,2) )
    contador = 1




class Avion(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="avion",vida= 2, cantidad = 3, tamaño = (4,3,2))
    contador = 1

class ElevadorEspacial(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="elevador espacial",vida=4, cantidad = 1, tamaño =(1,1,10)) 
    contador = 1




tablero = Tablero()
globo1 = Globo()
globo2 = Globo()
globo3 = Globo()
globo4 = Globo()
globo5 = Globo()
zeppelin1 = Zeppelin()
zeppelin2 = Zeppelin()
avion1 = Avion()
avion2 = Avion()
avion3 = Avion()
elevador_espacial1 = ElevadorEspacial()
vehiculos = [globo1, globo2, globo3, globo4, globo5, zeppelin1, zeppelin2, avion1, avion2, avion3, elevador_espacial1]
for vehiculo in vehiculos:
    tablero.colocar_Vehiculo(vehiculo,"Jugador1")
    tablero.mostrar_Tablero()
        
        



