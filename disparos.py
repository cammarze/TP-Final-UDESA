import numpy as np
import pruebo as pr

"""Buenas, aca asumo que la clase Tablero tiene como atributo:
    self.guardar_disparos = {}
falta agregar cosas como chequear si ya le pego en la coordenada ingresada pero bueno, 
lo voy subiendo por si ven algun error (ya que no lo prob;e, o si consideran que falta algo en este codigo)
"""

def disparo(self):
    ubicacion = pr.preguntar_coordenadas("Ingrese las coordenadas: ",
                                         "Coordenadas invalidas\nIngrese nuevamente las coordenadas: ",
                                         tamano=(self.dim_x, self.dim_y, self.dim_z))

    if self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] == 1:  #cheuqeo si hay un vehiculo en la coordenada ingresada

        vehiculos = [Avion(), Globo(), Zeppelin(), ElevadorEspacial()] #lista para iterar sobre las clases de los vehiculos
        for vehiculo in vehiculos: #itera dentro de los vehiculos y accede a la clase
            vehiculo.RecibirGolpe() #llama recibir golpe ya que el chabon recibio un golpe 
            if vehiculo.vida == 0: #si la vida LLEGa a 0, se ejecuta este if
                #marco que el vehiculo fue derrotado
                self.tablero[ubicacion[0], ubicacion[1], ubicacion[2]] = 0
                self.guardar_disparos[ubicacion] = "Sunk" #lo cAambie
                return self.guardar_disparos
            
        #el vehiculo fue tocado pero no derrotado    
        self.guardar_disparos[ubicacion] = "Hit"
        return self.guardar_disparos
    else:
        #no se hallo ningun vehiculp en la coordenada ingresada
        self.guardar_disparos[ubicacion] = "Miss"
        return self.guardar_disparos

   
