import numpy as np
import pruebo as pr

"""
    self.guardar_disparos = {}
"""

 def disparo(self):
        ubicacion = preguntar_coordenadas("Ingrese las coordenadas: ",
                                            "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ",
                                            tamano=(0,0,0))
        if ubicacion in self.guardar_disparos:
            print("Esta coordenada ya fue ingresada anteriormente")
            return self.disparo

        valor_coordenada = self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] #rcoordenada ingresada

        if valor_coordenada > 0: #chequeo si hay algun vehiculoo

            for v in vehiculos: #itero dentro de la lista vehiculos (por globo1, globo2, etc...)
                #chequeo si el valor de la coordenada coincide con los valores asocoiados a cada vehiculo
                if valor_coordenada == (1 + (v.contador/ 10)) or valor_coordenada == (2 + (v.contador/ 10)) or valor_coordenada == (3 + (v.contador / 10)) or valor_coordenada == 4:
                    v.vida -= 1 

                if v.vida == 0:
                    # Marcar que el vehículo fue derrotado
                    self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = -1 #le asigno un valor para que el cambio de colorcito
                    self.guardar_disparos[ubicacion] = "Sunk"
                    print("Resultado: < Hundido >")
                    return self.guardar_disparos
                
            #el vehiculo fue tocado pero no derrotado    
            self.guardar_disparos[ubicacion] = "Hit"
            print("Resultado: < Tocado >")
        else:
            #no se hallo ningun vehiculp en la coordenada ingresada
            self.guardar_disparos[ubicacion] = "Miss"
            print("Resultado: < Errado >")
            
        return self.guardar_disparos



   
