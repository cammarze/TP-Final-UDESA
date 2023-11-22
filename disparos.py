import numpy as np
import pruebo as pr

import funciones as f
import clases as c

"""
    self.guardar_vehiculos = {}
    self.guardar_disparos = {}
"""

def disparo(self,vehiculo, enemigo):
    ubicacion = f.preguntar_coordenadas("Ingrese las coordenadas: ",
                                        "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")
    
    while ubicacion in self.guardar_disparos: #Chequeo que el disparo no sea repetido
        print("Esta coordenada ya fue ingresada anteriormente.")
        ubicacion = f.preguntar_coordenadas("Ingrese las coordenadas nuevamente: ",
                                            "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ")

    valor_coordenada = enemigo.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] #Coordenada ingresada

    if valor_coordenada in enemigo.guardar_vehiculos: #Chequeo si hay algun vehiculo
        vehiculo.vida -= 1

        #El vehiculo fue tocado    
        self.guardar_disparos[ubicacion] = "Hit"
        self.disp_tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -2

        #El vehículo fue derribado
        if not vehiculo.vida:
            
            
            enemigo.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -3 #Le asigno un valor para que el cambio de colorcito
            self.guardar_disparos[ubicacion] = "Sunk"
            print("Resultado: < Hundido >")
        else:
            print("Resultado: < Tocado >")

    else: #No se hallo ningun vehiculo en la coordenada ingresada
        self.guardar_disparos[ubicacion] = "Miss"
        self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -1
        print("Resultado: < Errado >")
        



   
