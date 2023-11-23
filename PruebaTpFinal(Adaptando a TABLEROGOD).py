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
    

class Tablero:
    def _init_(self, dim_x=15, dim_y=15, dim_z=10):

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        self.tablero = np.zeros((dim_x, dim_y, dim_z))
        self.disp_tablero = np.zeros((dim_x,dim_y,dim_z))
        self.guardar_disparos = {} #Guarda lugares "disparados"
        self.guardar_vehiculos = {} #Guarda posicion de vehiculos


    def check_solapa(self,vehiculo, nuc_x,nuc_y,nuc_z):
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x #Invierto x e y
       
        if type(vehiculo) == Globo:
            return np.all(self.tablero[nuc_x - 1 : nuc_x + 2 , nuc_y - 1 : nuc_y + 2 , nuc_z - 1:nuc_z + 2]<=0) #Slicing de la posicion del globo a colocar
       
        elif type(vehiculo) == Zeppelin:
            check_x = [-2,3] #Chequeo 5 lugares
            check_y = [0,2] #Chequeo 2 lugares
            if vehiculo.rotacion in [90,270]:
                check_x, check_y = check_y, check_x
            return np.all(self.tablero[nuc_x + check_x[0] : nuc_x + check_x[1] , nuc_y + check_y[0] : nuc_y + check_y[1] , nuc_z : nuc_z + 2]<=0) #Slicing de la posicion del zeppelin a colocar
       
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
        if type(vehiculo) in [Avion, Zeppelin]: #Solo avion y zeppelin tienen rotacion
            if jugador == "Jugador1":
                num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
                while not num_rot.strip().isdecimal():
                    num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador}: ")
                num_rot = int(num_rot)
            else:
                num_rot = random.randint(0,25)
            vehiculo.rotacion = 90*num_rot%360 #Solo te puede dar 0, 90, 180, 270


    def colocar_Vehiculo(self, vehiculo, jugador):
        self.RotarVehiculo(vehiculo, jugador)
        textcoor = "(x y z)" if vehiculo.rotacion in [0,180] else "(y x z)" #Si rotacion 90 ó 270, coloque primero la y
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
            tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z) 
            tablero_pos += 1 + type(vehiculo).contador / 10
        elif type(vehiculo) == Zeppelin:
            tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            tablero_pos += 2 + type(vehiculo).contador / 10
        elif type(vehiculo) == Avion:
            tablero_pos1, tablero_pos2, tablero_pos3 = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            tablero_pos1 += 3 + type(vehiculo).contador / 10
            tablero_pos2 += 3 + type(vehiculo).contador / 10
            tablero_pos3 += 3 + type(vehiculo).contador / 10
        else:
            tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            tablero_pos += 4 
        type(vehiculo).contador += 1 #Cuenta la cantidad colocada de cada vehiculo

        self.guardar_vehiculos[self.tablero[nuc_x, nuc_y, nuc_z]] = (vehiculo, (nuc_x,nuc_y,nuc_z)) #Guarda la posicion del vehiculo colocado

      
    def agregar_colores(self):
        tablero_plt = np.copy(self.tablero).astype(int) #Copia el tablero pero con sus valores en int/enteros
        disp_tablero_plt = np.copy(self.disp_tablero).astype(int)
        colores = np.zeros(self.tablero.shape + (4,), dtype=np.float32) #Le agrega una cuarta dimension para poder meterle colores
        colores_disp = np.zeros(self.tablero.shape + (4,), dtype=np.float32)
        
        colores[tablero_plt == 1] = plt_colors.to_rgba("darkred", alpha=0.7)          #Globo
        colores[tablero_plt == 2] = plt_colors.to_rgba("midnightblue", alpha=0.7)     #Zeppelin
        colores[tablero_plt == 3] = plt_colors.to_rgba("lightgray", alpha=0.7)        #Avion
        colores[tablero_plt == 4] = plt_colors.to_rgba("darkslategray", alpha=0.7)    #Elevador espacial
        
        colores_disp[disp_tablero_plt == -1] = plt_colors.to_rgba("red", alpha=0.6)   #Miss
        colores_disp[disp_tablero_plt == -2] = plt_colors.to_rgba("green", alpha=0.6) #Hit
        colores_disp[disp_tablero_plt == -3] = plt_colors.to_rgba ("gray", alpha=0.4) #Sunk
        return colores, colores_disp 

    def disparo(self, enemigo):
        ubicacion = preguntar_coordenadas("Ingrese las coordenadas: ",
                                            "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")
        
        while ubicacion in self.guardar_disparos: #Chequeo que el disparo no sea repetido
            print("Esta coordenada ya fue ingresada anteriormente.")
            ubicacion = preguntar_coordenadas("Ingrese las coordenadas nuevamente: ",
                                                "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")

        valor_coordenada = enemigo.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] #Coordenada ingresada

        if valor_coordenada in enemigo.guardar_vehiculos: #Chequeo si hay algun vehiculo
            enemigo.guardar_vehiculos[valor_coordenada][0].vida -= 1

            #El vehiculo fue tocado    
            self.guardar_disparos[ubicacion] = "Hit"
            self.disp_tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -2

            #El vehículo fue derribado
            if not enemigo.guardar_vehiculos[valor_coordenada][0].vida:
                self.disp_tablero[enemigo.tablero == valor_coordenada] = -3 #Le asigno un valor para el cambio del colorcito
                enemigo.tablero[enemigo.tablero == valor_coordenada] = -3
                self.guardar_disparos[ubicacion] = "Sunk"
                print("Resultado: < Hundido >")
            else:
                print("Resultado: < Tocado >")

        else: #No se hallo ningun vehiculo en la coordenada ingresada
            self.guardar_disparos[ubicacion] = "Miss"
            self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -1
            print("Resultado: < Errado >")
    
    def mostrar_Tablero(self):
        colores, colores_disp = self.agregar_colores()
        fig, (ax1,ax2) = plt.subplots(1,2, subplot_kw={"projection": "3d"})
        fig.set_size_inches(6, 6)
        ax1.voxels(self.tablero, facecolors=colores , edgecolor='k') #Nuestro tablero
        ax2.voxels(self.disp_tablero, facecolors=colores_disp) #Tablero de nuestros disparos (tablero del enemigo)
        plt.show()


class Vehiculo:
    def _init_(self, nombre, vida, cantidad, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.cantidad = cantidad
        self.tamaño = tamaño
        self.rotacion = 0

    def derribado(self):
        return not self.vida

    def recibir_disparo(self): #HACER!
        self.vida -= 1
        if self.derribado():
            pass

class Globo(Vehiculo):
    def _init_(self):
        super()._init_(nombre="globo", vida=1, cantidad=5, tamaño=(3, 3, 3))
    contador = 1

    def Posicion_tablero(self, tablero, nuc_x, nuc_y, nuc_z):
        return tablero[nuc_x - 1: nuc_x + 2, nuc_y - 1: nuc_y + 2, nuc_z -1: nuc_z + 2]    
    

class Zeppelin(Vehiculo):
    def _init_(self) -> None:
        super()._init_(nombre="zeppelin", vida = 3, cantidad = 2, tamaño = (5,2,2) )
    contador = 1

    def Posicion_tablero(self, tablero, nuc_x, nuc_y, nuc_z):
        if self.rotacion in [0,180]:
            return tablero[nuc_x - 2: nuc_x + 3, nuc_y: nuc_y + 2, nuc_z : nuc_z + 2]
        else:
            return tablero[nuc_x: nuc_x + 2, nuc_y - 2: nuc_y + 3, nuc_z : nuc_z + 2]


class Avion(Vehiculo):
    def _init_(self) -> None:
        super()._init_(nombre="avion", vida= 2, cantidad = 3, tamaño = (4,3,2))
    contador = 1

    def Posicion_tablero(self,tablero, nuc_x, nuc_y, nuc_z):
        if self.rotacion in [0,90]:
            suma_1 = 1
            suma_2 = -1
        else:
                suma_1 = 0
                suma_2 = 2
        if self.rotacion in [0,180]:
            return (tablero[nuc_x - 1 : nuc_x + 3 , nuc_y, nuc_z], 
                    tablero[nuc_x + suma_1 , nuc_y - 1 : nuc_y + 2 , nuc_z], 
                    tablero[nuc_x + suma_2 , nuc_y, nuc_z + 1 : nuc_z + 2])
        else:
            return (tablero[nuc_x, nuc_y - 1 : nuc_y + 3, nuc_z], 
                    tablero[nuc_x - 1 : nuc_x + 2, nuc_y + suma_1, nuc_z], 
                    tablero[nuc_x, nuc_y + suma_2, nuc_z + 1 : nuc_z + 2])
        

class ElevadorEspacial(Vehiculo):
    def _init_(self) -> None:
        super()._init_(nombre="elevador espacial",vida=4, cantidad = 1, tamaño =(1,1,10)) 
        self.rotacion = 0
    contador = 1
    
    def Posicion_tablero(self,tablero, nuc_x, nuc_y, nuc_z):
        return tablero[nuc_x, nuc_y, 0 : 10]


#Cuerpo
def main():
    tablero = Tablero()
    enemigo = Tablero()
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
    vehiculos = [elevador_espacial1, avion1, avion2, avion3, globo1, globo2, globo3, globo4, globo5, zeppelin1, zeppelin2]
    for vehiculo in vehiculos:
        tablero.colocar_Vehiculo(vehiculo,"Jugador1")
        enemigo.colocar_Vehiculo(vehiculo,"Jugador2")
        tablero.mostrar_Tablero()
    enemigo.mostrar_Tablero()
    hola = input("Ingresa algo: ")
    while hola != "-1":
        tablero.disparo(enemigo)
        hola = input("Ingresa -1 cuando quieras salir del while: ")
        tablero.mostrar_Tablero()
        enemigo.mostrar_Tablero()

if __name__ == "__main__":
    main()






