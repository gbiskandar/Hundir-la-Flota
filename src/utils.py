# Entregable: Juego de Hundir la Flota con 2 jugadores, barcos aleatorios de diferente eslora, disparos manuales de Jugador 1 y disparos aleatorios de Jugador 2

import numpy as np
import random
import constants
import time
import sys

# Jugador 1 - manual
Matriz_Escondida = np.full(fill_value = " ", shape = (10, 10)) # donde están los barcos del oponente
Matriz_Juego = np.full(fill_value = " ", shape = (10, 10))
Matriz_Tusbarcos = np.full(fill_value = " ", shape = (10, 10)) #los barcos del jugador y los disparos del jugador2

# Jugador 2 - IA 
Matriz_Juego2 = np.full(fill_value = " ", shape = (10, 10)) #tablero que vería jugador 2


# Funcion que imprime el tablero
def imprime_tablero(tablero):
    print('   A B C D E F G H I J ')
    print(' ***********************')        
    fila_num=1
    for fila in tablero:
        if fila_num == 10:
            print("%d|%s|" % (fila_num, "|".join(fila)))
            fila_num += 1
        else : 
            print(" %d|%s|" % (fila_num, "|".join(fila))) 
            fila_num += 1
    print(' ***********************')
    print('   A B C D E F G H I J ')


# Funcion que dispara los barcos manualmente
def dispara_barcos():
    fila = input("Por favor ingresa una fila del 1-10: ")
    while fila not in ['1','2','3','4','5','6','7','8','9','10']:
        if fila == '11':
            pantalla_final()
        print("Por favor ingresa una fila valida\n")
        fila = input("Por favor ingresa una fila del 1-10: ")
    columna = input("Por favor ingresa una columna de la A - J: ").upper()
    while columna not in ['A','B','C','D','E','F','G','H','I','J']:
        print("Por favor ingresa una columna valida\n")
        columna = input("Por favor ingresa una columna de la A - J: ").upper()
    return int(fila)-1,constants.letra_indice[columna]

def dispara_auto():
    for disparo in range(1): # crea 1 disparo aleatorio
        disp_fila, disp_col=random.randint(0,9), random.randint(0,9)
        while Matriz_Juego2[disp_fila][disp_col] == 'X' or Matriz_Juego2[disp_fila][disp_col] == '-':
            disp_fila, disp_col = random.randint(0, 9), random.randint(0, 9)
    return disp_fila , disp_col


# Funcion que crea los barcos de diferente eslora y los marco con "O"
def crea_barcos(tablero):
    '''
    Devuelve un np.array con el tablero de la máquina, 
    generadas las posiciones aleatoriamente
    '''
    lista_esloras = constants.lista_esloras

    for eslora in lista_esloras:
        while True:
            direcc = random.choice(["h","v"])
            pos_inic = np.random.randint(10, size = 2)
            
            fila = pos_inic[0]
            colum = pos_inic[1]
            
            coors_h = tablero[fila,colum:colum+eslora]
            coors_v = tablero[fila:fila+eslora,colum]

            if direcc == "h" and 0 <= colum + eslora < 10 and 'O' not in coors_h and len(coors_h)==eslora:
                tablero[fila, colum: colum+ eslora] = 'O'
                break
            elif direcc == "v" and 0 <= fila + eslora < 10 and 'O' not in coors_v and len(coors_v)==eslora:
                tablero[fila:fila + eslora, colum] = 'O'
                break


def cuenta_barcos_disp(tablero):
    cuenta = 0
    for fila in tablero:
        for columna in fila:
            if columna =='X':
                cuenta += 1
    return cuenta

# ‘X’ indica que los barcos han sido disparados
# ‘-‘ indica que has disparado al oceano abierto
 # Se crea la matriz del segundo jugador 
#imprime_tablero(Matriz_Escondida)

def turnos():
    crea_barcos(Matriz_Escondida)
    crea_barcos(Matriz_Tusbarcos)
    turnos = 200
    jugador = constants.jugador
    while turnos > 0:
        if  cuenta_barcos_disp(Matriz_Juego) == sum(constants.lista_esloras): # total =  barcos x eslora
            imprime_tablero(Matriz_Juego)
            espera()
            print(constants.victoria)
            espera()
            break
        elif  cuenta_barcos_disp(Matriz_Juego2) == sum(constants.lista_esloras): #total =  barcos x eslora
            imprime_tablero(Matriz_Juego2)
            espera()
            print(constants.derrota)
            espera()
            break 
        elif jugador == "J1" :
            print("Turno: Jugador 1")
            print("Tus barcos:")
            imprime_tablero(Matriz_Tusbarcos)
            print("Disparos al oponente:")
            imprime_tablero(Matriz_Juego)
            fila,columna = dispara_barcos() # disparo manual Jugador 1
            espera(1)
            if Matriz_Juego[fila][columna]=='-':
                print("\nYa has adivinado ahí\n")
                espera(1)
            elif Matriz_Escondida[fila][columna]=='O':
                print(constants.explosion)
                Matriz_Juego[fila][columna]='X'
                espera()
                turnos -= 1
                continue #continua si acierta disparando a un barco
            else:
                print("\nHas fallado\n")
                Matriz_Juego[fila][columna] = '-'
                turnos -= 1
                espera()
                jugador = "J2"
                
        elif jugador == "J2" :
            print("Turno: Jugador 2")
            imprime_tablero(Matriz_Juego2)
            fila,columna = dispara_auto() # disparo automatico Jugador 2
            espera()
            if Matriz_Juego2[fila][columna]=='-':
                continue
            elif Matriz_Tusbarcos[fila][columna]=='O':
                print(constants.explosion)
                espera()
                Matriz_Juego2[fila][columna]='X'
                Matriz_Tusbarcos[fila][columna]='X'
                turnos -= 1
                continue # continua si acierta disparando a un barco
            else:
                print("\nHa fallado\n")
                espera(1)
                Matriz_Juego2[fila][columna] = '-'
                Matriz_Tusbarcos[fila][columna]='-'
                turnos -= 1
                jugador = "J1"
           
        

def espera(n=2):
    print(constants.mensaje_esperando)
    time.sleep(n)

def pantalla_final():
    espera()
    print(constants.mensaje_final)
    espera()
    sys.exit()
    
