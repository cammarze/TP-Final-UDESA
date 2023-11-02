# Trabajo Final - Pensamiento Computacional: WarGames 

#### `<link>` : <https://udesa-pc.github.io/tps/tpf/> 
##  Introduccion
El cielo ha sido un campo de batalla durante siglos. Desde los primitivos globos aerostáticos hasta modernas naves espaciales, el control de los cielos ha sido vital para establecer la supremacía en el campo de batalla. En este desafío, te enfrentarás en una batalla aérea en 3D utilizando globos, zepelines, aviones, y elevadores espaciales. Tu objetivo: derribar las unidades enemigas antes de que te derriben a ti.

## Especificaciones
### - Tablero de juego
+ Dimensiones del tablero  15 x 15 x 10
	+ **X**  y **Y**  representan la superficie horizontal.
	+ **Z**  representa la altura.
 
![](https://udesa-pc.github.io/tps/tpf/img/board.png)


| Vehiculo  | Cantidad | Resistencia (número de golpes) | Tamaño (celdas) | Forma |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| Globo  | 5 | 1 | 3x3x3 | ![](https://udesa-pc.github.io/tps/tpf/img/balloon.png) |
| Zeppelin  | 2 | 3 | 5x2x2 | ![](https://udesa-pc.github.io/tps/tpf/img/zeppelin.png) |
| Avión  | 3 | 2 | 4x3x2 (Forma “t”) | ![](https://udesa-pc.github.io/tps/tpf/img/plane.png) |
| Elevador Espacial  | 1 | 4 | 1x1x10 | ![](https://udesa-pc.github.io/tps/tpf/img/elevator.png) |

## Cómo Jugar
##### Momento Inicial
Cada jugador posiciona sus vehículos en el tablero. Los vehículos pueden ser rotados horizontalmente, pero no pueden superponerse. Los vehículos no pueden rotar verticalmente.

##### Desarrollo del Juego
El juego se desarrolla por turnos, donde cada jugador tiene oportunidad de realizar disparos contra el equipo oponente.

##### Turno de Juego:
+ **Disparo:** El jugador elige una coordenada para disparar.

+ **Resultado:** Se verifica si el disparo tocó algún vehículo enemigo. Si es así, se reduce en uno la resistencia del vehículo tocado. Si la resistencia de un vehículo llega a cero, es considerado “derribado”. Si un vehículo es derribado, se revelan todas las coordenadas ocupadas por el vehículo.

+ **Fin del Turno:** Una vez realizado el disparo, termina el turno del jugador y comienza el turno del oponente.

### Reglas del Juego
+ **Tocado:** Si una coordenada de un disparo coincide con una de las coordenadas ocupadas por un vehículo, se considera que ha sido “tocado”. La resistencia del vehículo se reduce en 1.

+ **Derribado:** Cuando la resistencia de un vehículo llega a cero debido a uno o varios “tocado”, el vehículo es considerado “derribado” y ya no participa en el juego.

+ **Tiro repetido:** Si un jugador dispara a una coordenada que ya ha sido disparada, no modifica la resistencia de ningún vehículo.

+ **Fin del Juego:** El juego termina cuando todos los vehículos de un jugador han sido “derribados”. El jugador con vehículos aún en juego es declarado ganador.

### Desarrollo
Se debe implementar un programa en Python que permita jugar a la batalla aérea. El programa debe permitir jugar contra la computadora. Se debe programar una estrategia para la computadora para que pueda competir contra el jugador humano. La estrategia debe incluír información de los últimos movimientos, disparos y estado de los vehículos.

Se deben implementar como mínimo las funciones con los siguientes prototipos para implementar el comportamiento de la computadora:

```python
def next_turn(hit_board: tuple) -> tuple:
   	 """Returns the coordinates to shoot next.

    Args:
        hit_board (tuple): A 3D iterable of strings representing the hit board.
        Each cell can be accessed by hit_board[x][y][z].

        Each cell has 4 possible values:
        - '?': No shot has been done there.
        - 'HIT': An airship has been hit there before.
        - 'MISS': A shot has been done there but did not hit any airship.
        - 'SUNK': An airship was there but has already been shot down entirely.

    Returns:
        tuple: (x,y,z) to shoot at.
    """
```
</pre>

```python
def get_starting_board():
   	 """
    Gives the board with the airships placed on it. The board is a 3D iterable of 
    strings. 

    Each cell has 12 possible values: 'EMPTY', 'BALLOON_0', 'BALLOON_1',
    'BALLOON_2', 'BALLOON_3' 'BALLOON_4', 'ZEPPELIN_0', 'ZEPPELIN_1', 'PLANE_0',
    'PLANE_1', 'PLANE_2', 'ELEVATOR'.

    Returns:
        tuple: A tuple of tuples of tuples of strings representing the board.
        Each cell can be accessed by board[x][y][z].
    """
```
</pre>
### Interfaz
La interfaz será principalmente a través de la línea de comando, donde los jugadores pueden ingresar coordenadas para disparar. Se espera una visualización en 3D utilizando matplotlib para mostrar el campo de batalla, los vehículos y el resultado de los disparos.

### Evaluación
Para aprobar, es fundamental que el código se ejecute correctamente sin lanzar excepciones; cumpliendo con los requerimientos de la consigna. Además, se evaluará la calidad del código y la calidad de los comentarios y documentación. Cualquier detalle adicional que agreguen será tenido en cuenta para la nota final.
