import numpy as np
import tkinter as tk
import random
import matplotlib.pyplot as plt
from OpGeneticas import generarHijos, mutarHijos, cruce_dos_puntos, seleccion_torneo, cruce_uniforme
from OpNonogramas import getFitness,crearPob
from interfaz import NonogramApp    

def graficar_aptitudes(best_aptitudes, average_aptitudes, worst_aptitudes):
    plt.figure(figsize=(10, 6))
    
    # Graficar las aptitudes
    plt.plot(best_aptitudes, label='Best Aptitude', color='green')
    plt.plot(average_aptitudes, label='Average Aptitude', color='blue')
    plt.plot(worst_aptitudes, label='Worst Aptitude', color='red')
    
    # Configuración de la gráfica
    plt.xlabel('Generation')
    plt.ylabel('Aptitude Score')
    plt.title('Evolution of Aptitudes Over Generations')
    plt.legend()
    plt.grid(True)
    
    # Mostrar la gráfica
    plt.show()

def genetico(tamPob,r, c, n, m, nColores, pbCruza, pbMutacion, opCruza,max_generaciones):
    
    best_aptitudes = []
    average_aptitudes = []
    worsts_aptitudes = []

    # Crear población inicial y evaluar aptitudes
    poblacion = crearPob(tamPob, n, m, nColores)
    aptitudesPoblacion = getFitness(poblacion, r, c, n, m, nColores)

    best_apt = min(aptitudesPoblacion)
    best_indi = aptitudesPoblacion.index(best_apt)

    best_aptitudes.append(best_apt)
    average_aptitudes.append(np.mean(aptitudesPoblacion))
    worsts_aptitudes.append(max(aptitudesPoblacion))

    i = 0
    generaciones_estancadas = 0  # Contador para generaciones sin cambios en la mejor aptitud

    while best_apt != 0 and best_apt != max(aptitudesPoblacion):
        padres = seleccion_torneo(poblacion, r, c, n, m, nColores, 5)

        # Cambiar el tipo de cruza dinámicamente
        if generaciones_estancadas > opCruza:
            # Cruza uniforme en generaciones iniciales
            hijos = generarHijos(padres, pbCruza,cruce_uniforme)
        else:
            # Cruza de dos puntos en generaciones avanzadas
            hijos = generarHijos(padres, pbCruza,cruce_dos_puntos)
        
        hijosMutados = mutarHijos(hijos, pbMutacion, nColores)
        nuevaPoblacion = poblacion + hijosMutados

        # Validación para asegurar que no se quede vacía
        if len(nuevaPoblacion) == 0:
            continue

        # Ordenar por aptitud y seleccionar los mejores
        nuevaPoblacion.sort(key=lambda ind: getFitness([ind], r, c, n, m, nColores)[0])
        poblacion = nuevaPoblacion[:tamPob]
    
        aptitudesPoblacion = getFitness(poblacion, r, c, n, m, nColores)

        # Actualizar la mejor aptitud
        nuevo_best_apt = min(aptitudesPoblacion)
        if nuevo_best_apt == best_apt:
            generaciones_estancadas += 1
        else:
            generaciones_estancadas = 0  # Reiniciar contador si hay mejora
        
        best_apt = nuevo_best_apt
        print(best_apt)
        best_indi = poblacion[0]

        # Si el mejor aptitud no mejora en 1000 generaciones, eliminar la mitad de la población y regenerar
        if generaciones_estancadas >= 1000:
            # Reemplazar un tercio de la población
            num_reemplazos = tamPob // 3  
            nueva_poblacion_parcial = crearPob(num_reemplazos, n, m, nColores)
            poblacion = poblacion[:tamPob - num_reemplazos] + nueva_poblacion_parcial
            pbMutacion=0.2 #Reinicia probabilidad de mutacion
            
        if nuevo_best_apt<best_apt:
            generaciones_estancadas=0

        pbMutacion = max(0.1, 1 - (i / max_generaciones))

        best_aptitudes.append(best_apt)
        average_aptitudes.append(np.mean(aptitudesPoblacion))
        worsts_aptitudes.append(max(aptitudesPoblacion))

        i += 1

    return best_aptitudes, average_aptitudes, worsts_aptitudes, i,best_indi

