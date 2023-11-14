import numpy as np
import pruebo as pr

"""
    self.guardar_disparos = {}
"""

def disparo(self):
    ubicacion = pr.preguntar_coordenadas("Ingrese las coordenadas: ",
                                         "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ",
                                         tamano=(0,0,0))
    
    if ubicacion in self.guardar_disparos:
        print("Esta coordenada ya fue ingresada anteriormente")
        return(disparo)

    if self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] == 1:  #cheuqeo si hay un vehiculo en la coordenada ingresada

        """
        Algun codigo en donde chequee que la vida es == 0, tengo que consultarle algo a debo y lo hago
        """
                #marco que el vehiculo fue derrotado
                self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = 0
                self.guardar_disparos[ubicacion] = "Sunk" 
                print("Resultado: < Hundido >")
            
        #el vehiculo fue tocado pero no derrotado    
        self.guardar_disparos[ubicacion] = "Hit"
        print("Resultado: < Tocado >")
    else:
        #no se hallo ningun vehiculp en la coordenada ingresada
        self.guardar_disparos[ubicacion] = "Miss"
        print("Resultado: < Errado >")
        
    return self.guardar_disparos


   
