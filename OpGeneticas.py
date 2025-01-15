import random
import numpy as np
from OpNonogramas import getFitness,arrayAMatriz,MatrizAArray


def cruce_dos_puntos(padre1, padre2):
    # Asegurar que ambos padres tengan el mismo tamaño
    assert len(padre1) == len(padre2), "Los padres deben tener el mismo tamaño"
    
    # Seleccionar dos puntos de cruce aleatorios sin que sean iguales
    punto1, punto2 = sorted(random.sample(range(1, len(padre1)), 2))

    # Crear hijos cruzando segmentos de los padres
    hijo1 = padre1[:punto1] + padre2[punto1:punto2] + padre1[punto2:]
    hijo2 = padre2[:punto1] + padre1[punto1:punto2] + padre2[punto2:]
    
    return hijo1, hijo2


def cruce_uniforme(padre1, padre2, prob=0.5):
    # Asegurar que ambos padres tengan el mismo tamaño
    assert len(padre1) == len(padre2), "Los padres deben tener el mismo tamaño"
    longitud = len(padre1)
    hijo1 = []
    hijo2 = []
    
    for i in range(longitud):
        if random.random() < prob:
            # Probabilidad de 0.5 para intercambiar el gen
            hijo1.append(padre1[i])
            hijo2.append(padre2[i])
        else:
            hijo1.append(padre2[i])
            hijo2.append(padre1[i])
    
    return hijo1, hijo2

def seleccion_torneo(poblacion, r, c, n, m, nColores, k=3):
    padres = []
    aptitudes = getFitness(poblacion, r, c, n ,m,nColores)

    for _ in range(len(poblacion)):
        # Seleccionar 'k' individuos aleatoriamente para el torneo
        indices_torneo = np.random.choice(len(poblacion), k, replace=False)
        # Buscar el individuo con la mejor aptitud dentro del torneo
        mejor_aptitud = float('inf')
        mejor_individuo = None

        for i in indices_torneo:
            if aptitudes[i] < mejor_aptitud:
                mejor_aptitud = aptitudes[i]
                mejor_individuo = poblacion[i]
        
        padres.append(mejor_individuo)

    return padres


def generarHijos(padres, pbCruza, opCruza):
    hijos=[]

    for i in range(len(padres)):
        pc=np.random.random()

        ind1 = np.random.randint(len(padres))
        ind2 = np.random.randint(len(padres))
        if pc <= pbCruza:

            padre1= MatrizAArray(padres[ind1])
            padre2= MatrizAArray(padres[ind2])

            hijo1, hijo2 = opCruza(padre1, padre2)
            

            hijo1=arrayAMatriz(hijo1, len(padres[0]),len(padres[0][0]))
            hijo2=arrayAMatriz(hijo2, len(padres[0]),len(padres[0][0]))

            hijos.append(hijo1)
            hijos.append(hijo2)
    
    return hijos


def mutarHijos(hijos, pbMutacion, numColores):
    hijosMutados = []

    for hijo in hijos:
        hijoMutado = []

        # Convertir el hijo a un arreglo para facilitar la mutación
        hijo = MatrizAArray(hijo)

        for i in range(len(hijo)):
            pm = np.random.random()
            if pm <= pbMutacion:
                # Mutar el valor actual a un nuevo color aleatorio diferente, considerando las pistas
                nuevoValor = np.random.randint(0, numColores+1)
                while nuevoValor == hijo[i]:  # Asegurar que sea diferente
                    nuevoValor = np.random.randint(0, numColores+1)
                hijoMutado.append(nuevoValor)
            else:
                hijoMutado.append(hijo[i])

        # Convertir el hijo mutado de vuelta a matriz
        hijoMutado = arrayAMatriz(hijoMutado, len(hijos[0]), len(hijos[0][0]))
        hijosMutados.append(hijoMutado)

    return hijosMutados
