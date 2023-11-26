import clases as c

def main():
    tablero = c.Tablero()
    enemigo = c.Tablero()
    globo1 = c.Globo()
    globo2 = c.Globo()
    globo3 = c.Globo()
    globo4 = c.Globo()
    globo5 = c.Globo()
    zeppelin1 = c.Zeppelin()
    zeppelin2 = c.Zeppelin()
    avion1 = c.Avion()
    avion2 = c.Avion()
    avion3 = c.Avion()
    elevador_espacial1 = c.ElevadorEspacial()

    enemigo_globo1 = c.Globo()
    enemigo_globo2 = c.Globo()
    enemigo_globo3 = c.Globo()
    enemigo_globo4 = c.Globo()
    enemigo_globo5 = c.Globo()
    enemigo_zeppelin1 = c.Zeppelin()
    enemigo_zeppelin2 = c.Zeppelin()
    enemigo_avion1 = c.Avion()
    enemigo_avion2 = c.Avion()
    enemigo_avion3 = c.Avion()
    enemigo_elevador_espacial1 = c.ElevadorEspacial()
    vehiculos = [globo1, globo2, globo3, globo4, globo5, zeppelin1, zeppelin2,  avion1, avion2, avion3,elevador_espacial1]
    enem_vehiculos = [enemigo_globo1, enemigo_globo2, enemigo_globo3, enemigo_globo4, enemigo_globo5, enemigo_zeppelin1, enemigo_zeppelin2,  enemigo_avion1, enemigo_avion2, enemigo_avion3,enemigo_elevador_espacial1]

    for vehiculo in vehiculos:
        tablero.colocar_Vehiculo(vehiculo,"Jugador0")
        tablero.mostrar_Tablero()

    for enem_vehiculo in enem_vehiculos:    
        enemigo.colocar_Vehiculo(enem_vehiculo,"Jugador2")

    while True:
        tablero.disparo(enemigo, "Jugador1")
        tablero.mostrar_Tablero()
        if enemigo.cantidad_vehiculos == 0:
            print("Ganador Jugador 1")
            break
        enemigo.disparo(tablero, "jugador2")
        if tablero.cantidad_vehiculos == 0:
            print("Ganador Jugador 2")
            break
        
    tablero.mostrar_Tablero()
    enemigo.mostrar_Tablero()

if __name__ == "__main__":
    main()