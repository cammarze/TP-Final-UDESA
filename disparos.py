import numpy as np
import pruebo as pr

import codigo_entero as c


def disparo(self, enemigo):
    ubicacion = c.preguntar_coordenadas("Ingrese las coordenadas: ",
                                        "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")
    
    while ubicacion in self.guardar_disparos: #Chequeo que el disparo no sea repetido
        print("Esta coordenada ya fue ingresada anteriormente.")
        ubicacion = c.preguntar_coordenadas("Ingrese las coordenadas nuevamente: ",
                                            "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")

    valor_coordenada = enemigo.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] #Coordenada ingresada

    if valor_coordenada in enemigo.guardar_vehiculos: #Chequeo si hay algun vehiculo
        enemigo.guardar_vehiculos[valor_coordenada][0].vida -= 1

        #El vehiculo fue tocado    
        self.guardar_disparos[ubicacion] = "Hit"
        self.disp_tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -2

        #El vehículo fue derribado
        if not  enemigo.guardar_vehiculos[valor_coordenada][0].vida:
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
        



   
