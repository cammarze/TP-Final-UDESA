import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as plt_colors
import funciones as f

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

        
    def check_solapa(self,vehiculo: object, nuc_x: int,nuc_y:int,nuc_z:int) -> bool:
        """
        Chequea superposicion entre los vehiculos
        Args:
        - vehiculo: Vehiculo que se ubica en el tablero.
        - nuc_x: coordenada X del nulceo del vehiculo.
        - nuc_y: coordenada Y del nulceo del vehiculo.
        - nuc_z: coordenada Z del nucleo del vehiculo.

        Returns:
        - bool --> True si los vehiculos no se superponen, False si hay solapamiento.
        """
        if vehiculo.rotacion in [90,270]:
            nuc_x, nuc_y = nuc_y, nuc_x #Invierto x e y

        if type(vehiculo) == Avion: #Slicing de la posicion del avion a colocar
            tablero_pos1, tablero_pos2, tablero_pos3 = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            return np.all(tablero_pos1<=0) and np.all(tablero_pos2 <= 0) and np.all(tablero_pos3<=0)  
        else: #Slicing de la posicion del vehiculo a colocar
            Tablero_pos = vehiculo.Posicion_tablero(self.tablero, nuc_x, nuc_y, nuc_z)
            return np.all(Tablero_pos<=0)
       
    def RotarVehiculo(self, vehiculo:object, jugador: str) -> None:
        """
        Rota el vehiculo
        Para "Jugador1" --> pregunta al jugador la cantidad de veces que lo desea rotar
        Para "Jugador2" (computadora) --> De forma aleatoria
        - La rotacion se realiza unicamente para el Avion y el Zeppelin
        Args:
        - vehiculo: vehiculo que se va rotar 
        - jugador: jugador actual ("jugador1", "jugador2")
        
        """
        if type(vehiculo) in [Avion, Zeppelin]: #Solo avion y zeppelin tienen rotacion
            if jugador == "Jugador1":
                num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador + 1} 90°: ")
                while not num_rot.strip().isdecimal():
                    num_rot = input(f"Ingrese la cantidad de veces que quiere rotar el {vehiculo.nombre} {vehiculo.contador + 1} 90°: ")
                num_rot = int(num_rot)
            else:
                num_rot = random.randint(0,25)
            vehiculo.rotacion = 90*num_rot%360 #Solo te puede dar 0, 90, 180, 270


    def colocar_Vehiculo(self, vehiculo: object, jugador: str) -> None:
        """
        Ubica los vehiculos segun coordenadas ingresadas
        ------------------------------------------------
        Realiza la rotacion de los vehiculos utilizando la funcion 'RotarVehiculo'
        Chequea la posible superoposicion entre vehiculos mediante 'check_solapa'
        Ajusta la posicion del vehiculo en el tablero y actualiza el contador de vehiculos

        Args:
        - vehiculo: vehiculo que se va a ubicar
        - jugador: jugador actual ("jugador1", "jugador2")
        """
        self.RotarVehiculo(vehiculo, jugador)
        textcoor = "(x y z)" if vehiculo.rotacion in [0,180] else "(y x z)" #Si rotacion 90 ó 270, coloque primero la y
        nuc_x, nuc_y, nuc_z = f.preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador + 1} {textcoor}: ",
                                     f"Datos invalidos\nIngrese el nucleo de {vehiculo.nombre} {vehiculo.contador + 1} {textcoor}: ",jugador,
                                     vehiculo.tamaño)
        
        while not self.check_solapa(vehiculo, nuc_x, nuc_y, nuc_z):
            if jugador == "Jugador1":
                print("Solapamiento entre vehiculos. Ingrese otra vez")
            nuc_x, nuc_y, nuc_z = f.preguntar_coordenadas(f"-{vehiculo.nombre} #{vehiculo.contador + 1} {textcoor}: ", 
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
   

    def agregar_colores(self) -> tuple[np.ndarray]:
        """
        Le asigna colores asociados a los distintos tipos de vehiculos ubicado en el tablero
        --------------------------------------------------------------------------
        Se crea una copia del tablero y del tablero de disparos 
        Tambien se le asigna colores a los disparos realizado segun su estado (Miss, Hit, Sunk)
        Returns:
        - colores --> Array con los colores asociados a los vehiculos
        - colores_disp --> Array con los colores para representar los estados de los disparos
        """
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
    


    def disparo(self, enemigo: object, jugador:object) -> None:
        """
        Realiza un disparo sobre el tablero enemigo
        -------------------------------------------
        Se solicita al jugador coordenadas para el disparo y chequea si fue ingresada
        Si el disparo el disparo cooincide con la ubicacion del vehiculo (impacta) actualiza el estado (Hit o Sunk)
        Actualiza el registro de los disparos realizados y muestra el resultado

        Args:
        - enemigo: Tablero del enemigo
        - jugador: Identifica que jugador realiza el disparo ("jugador1" o "jugador2")

        Note:
        -Para "Jugador2" (computadora) si los vehiculos fueron derrotados, excepto el Elevador Espacial, los disparos son aleatorios.
        Si encuentra un 'HIT', incrmenta la coordenada z en 1.
        """
        coor_x, coor_y, coor_z = f.preguntar_coordenadas("Ingrese las coordenadas del disparo: ",
                                                        "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ", jugador)

        
        #Chequeo que el disparo no sea repetido
        while (coor_x, coor_y, coor_z) in self.guardar_disparos or enemigo.tablero[coor_x, coor_y, coor_z] < 0:
            if jugador == "jugador1":
                if enemigo.tablero[coor_x, coor_y, coor_z] < 0:
                    print("Disparo sobre vehiculo derribado")
                else:
                    print("Esta coordenada ya fue ingresada anteriormente.")

            coor_x, coor_y, coor_z = f.preguntar_coordenadas("Ingrese las coordenadas del disparo nuevamente: ",
                                                    "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ", jugador)

                
        print(jugador.title())
        #Coordenada ingresada
        valor_coordenada = enemigo.tablero[coor_x, coor_y, coor_z]
        
        #Chequeo si hay algun vehiculo
        if valor_coordenada in enemigo.guardar_vehiculos: 
            enemigo.guardar_vehiculos[valor_coordenada].recibir_disparo()

            #El vehiculo fue tocado    
            self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Hit"
            self.disp_tablero[coor_x, coor_y, coor_z] = -2

            #El vehículo fue derribado
            if enemigo.guardar_vehiculos[valor_coordenada].derribado():
                self.disp_tablero[enemigo.tablero == valor_coordenada] = -3 #Le asigno un valor para el cambio del colorcito
                enemigo.tablero[enemigo.tablero == valor_coordenada] = -3
                self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Sunk"
                if jugador != "Jugador1":
                    print(f"Coordenadas: < {coor_x} {coor_y} {coor_z} >")
                print(f"Resultado: < {enemigo.guardar_vehiculos[valor_coordenada].nombre.title()} Hundido a favor de {jugador}>")
                enemigo.cantidad_vehiculos -= 1
            else:
                if jugador != "Jugador1":
                    print(f"Coordenadas: < {coor_x} {coor_y} {coor_z} >")
                print("Resultado: < Tocado >")

        else: #No se hallo ningun vehiculo en la coordenada ingresada
            self.guardar_disparos[(coor_x, coor_y, coor_z)] = "Miss"
            self.disp_tablero[coor_x, coor_y, coor_z] = -1
            if jugador != "Jugador1":
                print(f"Coordenadas: < {coor_x} {coor_y} {coor_z} >")
            print("Resultado: < Errado >")
        print("-------------------------")


    def mostrar_Tablero(self) -> None:
        """

        Muestra los tableros del juego 
        ------------------------------
        Realiza una representacion visual de dos tableros
        El subgrafico de la izquierda mustra estado actual del tablero del jugador
        El subgrafico de la derecha muestra el tablero de disparos realizados hacia el enemigo

        """
        colores, colores_disp = self.agregar_colores()
        fig, (ax1,ax2) = plt.subplots(1,2, subplot_kw={"projection": "3d"})
        fig.set_size_inches(11, 6)

        ax1.set_title ('Player Board',fontsize=12, color='black') 
        ax1.voxels(self.tablero, facecolors=colores , edgecolor='k') #Nuestro tablero

        ax2.set_title ('Hit Board',fontsize=12, color='black') 
        ax2.voxels(self.disp_tablero, facecolors=colores_disp) #Tablero de nuestros disparos (tablero del enemigo)
        plt.show()


class Vehiculo:
    def __init__(self, nombre, vida, tamaño):
        self.nombre = nombre
        self.vida = vida
        self.tamaño = tamaño
        self.rotacion = 0

    def derribado(self) -> bool: #si el vehiculo fue derribado o no
        return not self.vida #True si el vehiculo fue derribado, False caso contrario
    
    def recibir_disparo(self): 
        self.vida -= 1


class Globo(Vehiculo):
    def __init__(self):
        super().__init__(nombre="globo", vida=1, tamaño=(3, 3, 3))
    contador = 0

    def Posicion_tablero(self, tablero: object, nuc_x: int, nuc_y: int, nuc_z:int) -> np.ndarray:
        """
        retorna la posicion actual del globo en el tablero

        Args:
        - tablero: Tablero de juego
        - nuc_x, nuc_y, nuc_z: Coordenadas del nucleo del globo

        Returns:
        - Seccion del tablero que representa la posicion del globo en funcion de sus coordenadas
        """
        return tablero[nuc_x - 1: nuc_x + 2, nuc_y - 1: nuc_y + 2, nuc_z -1: nuc_z + 2] 
       

class Zeppelin(Vehiculo):
    
    def __init__(self) -> None:
        super().__init__(nombre="zeppelin", vida = 3, tamaño = (5,2,2) )
    contador = 0

    def Posicion_tablero(self, tablero:object, nuc_x:int, nuc_y:int, nuc_z:int) -> np.ndarray:
        """
        retorna la posicion actual del Zeppelin en el tablero

        Args:
        - tablero: Tablero de juego
        - nuc_x, nuc_y, nuc_z: Coordenadas del nucleo del zeppelin

        Returns:
        - Seccion del tablero que representa la posicion del zeppelin en funcion de sus coordenadas y su rotacion
        """
        if self.rotacion in [0,180]:
            return tablero[nuc_x - 2: nuc_x + 3, nuc_y: nuc_y + 2, nuc_z : nuc_z + 2]
        else:
            return tablero[nuc_x: nuc_x + 2, nuc_y - 2: nuc_y + 3, nuc_z : nuc_z + 2]
        

class Avion(Vehiculo):
    def __init__(self) -> None:
        super().__init__(nombre="avion", vida= 2, tamaño = (4,3,2))
    contador = 0

    def Posicion_tablero(self,tablero:object, nuc_x:int, nuc_y:int, nuc_z:int) -> tuple[np.ndarray]:
        """
        retorna la posicion actual del Avion en el tablero

        Args:
        - tablero: Tablero de juego
        - nuc_x, nuc_y, nuc_z: Coordenadas del nucleo del zeppelin

        Returns:
        - Seccion del tablero que representa la posicion del avion en funcion de sus coordenadas y su rotacion
        """
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
    def Posicion_tablero(self,tablero: object, nuc_x: int, nuc_y: int, nuc_z: int) -> np.ndarray:
        """
        retorna la posicion actual del Elevador Espacial en el tablero

        Args:
        - tablero: Tablero de juego
        - nuc_x, nuc_y, nuc_z: Coordenadas del nucleo del Elevador Espacial

        Returns:
        - Seccion del tablero que representa la posicion del Elevador Espacial en funcion de sus coordenadas
        """
        return tablero[nuc_x, nuc_y, 0 : 10]
