# Modo de Juego #

# Colocacion de vehiculos
Para colocar los vehiculos, el programa le pedira que ingrese 3 coordenadas (x, y, z). Estas corresponden al nucleo del vehiculo que se desea colocar. Las coordenadas deberan ser
ingresadas en una misma linea, separadas por espacios (por ej: 5 5 5). Los valores maximos y minimos para las coordenadas del nucleo varian segun el vehiculo que quiera colocar.
Tenga en cuenta que los valores maximos y minimos de (x, y) son 14 y 0, respectivamente, y el valor maximo y minimo de z es 9 y 0, respectivamente.
Tambien se le pedira la rotacion del vehiculo. Debera ingresar cuantas veces lo quiere rotar 90°. Si no quiere rotarlo, debe ingresar 0 (o un multiplo de 4). Si desea rotarlo 90°,
debe ingresar 1 (o 1 + cualquier multiplo de 4).Si desea rotarlo 180°, debe ingresar 2 (o 2 + cualquier multiplo de 4). Por ultimo, si quiere rotarlo 270°, debe ingresar 3 (o 3 + cualquier
multiplo de 4). En esencia, el modulo entre el numero ingresado y 4 determinara la rotacion del vehiculo.

# Desarrollo
Una vez colocados los vehiculos, se inicia la partida. Esta se desarrolla por turnos. En cada turno, el jugador debe ingresar las coordenadas a disparar. Estas deben ser ingresadas
en una misma linea, separadas por espacios. Luego, se imprimira en pantalla el resultado del disparo. Este puede ser Errado (no habia ningun vehiculo), Tocado (habia un vehiculo pero
este no fue derribado) o Hundido (habia un vehiculo y fue derribado). Si se ingresara una coordenada (x, y, z) que ya fue utilizida anteriormente o en la que se encuentra un vehiculo
hundido, se solicitara que se ingrese la coordenada nuevamente. El juego termina cuando todos los vehiculos de un jugador hayan sido derribados. El ganador es el jugador que aun tiene
vehiculos en pie.
