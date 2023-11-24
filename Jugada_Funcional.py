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
    def __init__(self, dim_x=15, dim_y=15, dim_z=10):

        self.dim_x = dim_x
        self.dim_y = dim_y
        self.dim_z = dim_z
        self.tablero = np.zeros((dim_x, dim_y, dim_z))
        self.disp_tablero = np.zeros((dim_x,dim_y,dim_z))
        self.cantidad_vehiculos = 11
        self.guardar_disparos = {} #Guarda lugares "disparados"
        self.guardar_vehiculos = {} #Guarda posicion de vehiculos

        
    def check_solapa(self,vehiculo, nuc_x,nuc_y,nuc_z):
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x #Invierto x e y

        if type(vehiculo) == Avion:
            tablero_pos1, tablero_pos2, tablero_pos3 = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z) #Slicing de la posicion del avion a colocar
            return np.all(tablero_pos1<=0) and np.all(tablero_pos2 <= 0) and np.all(tablero_pos3<=0)  
        else:
            Tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z) #Slicing de la posicion del vehiculo a colocar
            return np.all(Tablero_pos<=0)  
       

    def RotarVehiculo(self, vehiculo, jugador):
        if type(vehiculo) in [Avion, Zeppelin]: #Solo avion y zeppelin tienen rotacion
            if jugador == "Jugador1":
                num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador} 90°: ")
                while not num_rot.strip().isdecimal():
                    num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador} 90°: ")
                num_rot = int(num_rot)
            else:
                num_rot = random.randint(0,25)
            vehiculo.rotacion = 90*num_rot%360 #Solo te puede dar 0, 90, 180, 270


    def colocar_Vehiculo(self, vehiculo, jugador):
        self.RotarVehiculo(vehiculo, jugador)
        textcoor = "(x y z)" if vehiculo.rotacion in [0,180] else "(y x z)" #Si rotacion 90 ó 270, coloque primero la y
        nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador + 1} {textcoor}: ",
                                     f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador + 1} {textcoor}: ",jugador,
                                     vehiculo.tamaño)
        
        while not self.check_solapa(vehiculo, nuc_x, nuc_y, nuc_z):
            if jugador == "Jugador1":
                print("Solapamiento entre vehiculos. Ingrese otra vez")
            nuc_x, nuc_y, nuc_z = preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador + 1} {textcoor}: ", 
                                                        f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador + 1} {textcoor}: ",jugador,
                                                        vehiculo.tamaño)
            
        dict_valor = {Globo : 1, Zeppelin : 2, ElevadorEspacial : 4}
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x

        if type(vehiculo) == Avion:
            tablero_pos1, tablero_pos2, tablero_pos3 = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            tablero_pos1 += 3 + vehiculo.contador / 10
            tablero_pos2 += 3 + vehiculo.contador / 10
            tablero_pos3 += 3 + vehiculo.contador / 10
            self.tablero[self.tablero == (3 + type(vehiculo).contador / 10)*2] = 3 + vehiculo.contador / 10
        else:
            tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z) 
            tablero_pos += dict_valor[type(vehiculo)] + vehiculo.contador / 10

        type(vehiculo).contador += 1 #Cuenta la cantidad colocada de cada vehiculo
        self.guardar_vehiculos[self.tablero[nuc_x, nuc_y, nuc_z]] = vehiculo #Guarda la posicion del vehiculo colocado    
   

    def agregar_colores(self):
        tablero_plt = np.copy(self.tablero).astype(int) #Copia el tablero pero con sus valores en int/enteros
        disp_tablero_plt = np.copy(self.disp_tablero).astype(int)
        colores = np.zeros(self.tablero.shape + (4,), dtype=np.float32) #Le agrega una cuarta dimension para poder meterle colores
        colores_disp = np.zeros(self.tablero.shape + (4,), dtype=np.float32)

        colores[tablero_plt == 1] = plt_colors.to_rgba("darkred", alpha=0.7)          #Globo
        colores[tablero_plt == 2] = plt_colors.to_rgba("midnightblue", alpha=0.7)     #Zeppelin
        colores[tablero_plt == 3] = plt_colors.to_rgba("lightgray", alpha=0.7)        #Avion
        colores[tablero_plt == 4] = plt_colors.to_rgba("darkslategray", alpha=0.7)    #Elevador espacial
        colores[tablero_plt == -3] = plt_colors.to_rgba ("gray", alpha=0.4)

        colores_disp[disp_tablero_plt == -1] = plt_colors.to_rgba("red", alpha=0.4)   #Miss
        colores_disp[disp_tablero_plt == -2] = plt_colors.to_rgba("green", alpha=0.4) #Hit
        colores_disp[disp_tablero_plt == -3] = plt_colors.to_rgba ("gray", alpha=0.4) #Sunk

        return colores, colores_disp 
    

    def disparo(self, enemigo, jugador):

        coor_x, coor_y, coor_z = preguntar_coordenadas("Ingrese las coordenadas: ",
                                            "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ", jugador)
        
       
        while (coor_x, coor_y, coor_z) in self.guardar_disparos or enemigo.tablero[coor_x, coor_y, coor_z] < 0: #Chequeo que el disparo no sea repetido

            if jugador == "Jugador1":
                if enemigo.tablero[coor_x, coor_y, coor_z] < 0:
                    print("Disparo sobre vehiculo derribado")
                else:
                    print("Esta coordenada ya fue ingresada anteriormente.")

            coor_x, coor_y, coor_z = preguntar_coordenadas("Ingrese las coordenadas nuevamente: ",
                                                "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ", jugador)
            
        valor_coordenada = enemigo.tablero[coor_x, coor_y, coor_z] #Coordenada ingresada

        if valor_coordenada in enemigo.guardar_vehiculos: #Chequeo si hay algun vehiculo
            enemigo.guardar_vehiculos[valor_coordenada].recibir_disparo()

            #El vehiculo fue tocado    
            self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Hit"
            self.disp_tablero[coor_x, coor_y, coor_z] = -2

            #El vehículo fue derribado
            if enemigo.guardar_vehiculos[valor_coordenada].derribado():
                self.disp_tablero[enemigo.tablero == valor_coordenada] = -3 #Le asigno un valor para el cambio del colorcito
                enemigo.tablero[enemigo.tablero == valor_coordenada] = -3
                self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Sunk"
                print(f"Resultado: < {enemigo.guardar_vehiculos[valor_coordenada].nombre.title()} Hundido a favor de {jugador}>")
                enemigo.cantidad_vehiculos -= 1
            else:
                if jugador == "Jugador1":
                    print("Resultado: < Tocado >")

        else: #No se hallo ningun vehiculo en la coordenada ingresada
            self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Miss"
            self.disp_tablero[coor_x, coor_y, coor_z] = -1
            if jugador == "Jugador1":
                print("Resultado: < Errado >")


    def mostrar_Tablero(self):
        colores, colores_disp = self.agregar_colores()
        fig, (ax1,ax2) = plt.subplots(1,2, subplot_kw={"projection": "3d"})
        fig.set_size_inches(11, 6)
        
        ax1.voxels(self.tablero, facecolors=colores , edgecolor='k') #Nuestro tablero
        ax2.voxels(self.disp_tablero, facecolors=colores_disp) #Tablero de nuestros disparos (tablero del enemigo)
        plt.show()


class Vehiculo:
    def __init__(self, nombre, vida, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.tamaño = tamaño
        self.rotacion = 0

    def derribado(self):
        return not self.vida
    
    def recibir_disparo(self): #HACER!
        self.vida -= 1


class Globo(Vehiculo):
    def __init__(self):
        super().__init__(nombre="globo", vida=1, tamaño=(3, 3, 3))
    contador = 0

    def Posicion_tablero(self, tablero, nuc_x, nuc_y, nuc_z):
        return tablero[nuc_x - 1: nuc_x + 2, nuc_y - 1: nuc_y + 2, nuc_z -1: nuc_z + 2] 
       

class Zeppelin(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="zeppelin", vida = 3, tamaño = (5,2,2) )
    contador = 0

    def Posicion_tablero(self, tablero, nuc_x, nuc_y, nuc_z):
        if self.rotacion in [0,180]:
            return tablero[nuc_x - 2: nuc_x + 3, nuc_y: nuc_y + 2, nuc_z : nuc_z + 2]
        else:
            return tablero[nuc_x: nuc_x + 2, nuc_y - 2: nuc_y + 3, nuc_z : nuc_z + 2]
        

class Avion(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="avion", vida= 2, tamaño = (4,3,2))
    contador = 0

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
    def __init__(self) -> None:
        super().__init__(nombre="elevador espacial",vida=4, tamaño =(1,1,10)) 
    contador = 0
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

    enemigo_globo1 = Globo()
    enemigo_globo2 = Globo()
    enemigo_globo3 = Globo()
    enemigo_globo4 = Globo()
    enemigo_globo5 = Globo()
    enemigo_zeppelin1 = Zeppelin()
    enemigo_zeppelin2 = Zeppelin()
    enemigo_avion1 = Avion()
    enemigo_avion2 = Avion()
    enemigo_avion3 = Avion()
    enemigo_elevador_espacial1 = ElevadorEspacial()
    vehiculos = [globo1, globo2, globo3, globo4, globo5, zeppelin1, zeppelin2,  avion1, avion2, avion3,elevador_espacial1]
    enem_vehiculos = [enemigo_globo1, enemigo_globo2, enemigo_globo3, enemigo_globo4, enemigo_globo5, enemigo_zeppelin1, enemigo_zeppelin2,  enemigo_avion1, enemigo_avion2, enemigo_avion3,enemigo_elevador_espacial1]
    for vehiculo in vehiculos:
        tablero.colocar_Vehiculo(vehiculo,"Jugador0")
    for enem_vehiculo in enem_vehiculos:    
        enemigo.colocar_Vehiculo(enem_vehiculo,"Jugador2")
    tablero.mostrar_Tablero()
    enemigo.mostrar_Tablero()
    while True:
        tablero.disparo(enemigo, "Jugador2")
        if enemigo.cantidad_vehiculos == 0:
            break
        enemigo.disparo(tablero, "jugador3")
        if tablero.cantidad_vehiculos == 0:
            break

    tablero.mostrar_Tablero()
    enemigo.mostrar_Tablero()

if __name__ == "__main__":
    main()