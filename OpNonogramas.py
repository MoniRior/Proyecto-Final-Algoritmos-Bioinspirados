import random
import numpy as np

def arrayAMatriz(arreglo, n,m):
    if len(arreglo) != n * m:
        raise ValueError("El tamaño del arreglo no coincide con el tamaño de la matriz n x n")
    matriz = np.array(arreglo).reshape(n, m)

    return matriz

def MatrizAArray(matriz):
    arreglo_plano = matriz.flatten().tolist()
    return arreglo_plano

def crearPob(tamPob,n,m,nColores):
    poblacion = [crearIndiv(n,m,nColores) for _ in range(tamPob)]
    return poblacion


def crearIndiv(n,m,nColores=4):
    indi=np.random.randint(0, nColores+1, size=(n,m))
    return indi

#Aptitud de la poblacion
def getFitness(poblacion, r, c,n,m,nColores=4):
    aptitudes = []
    for i in range(len(poblacion)):
        indi=poblacion[i]
        rS, cS=getIndSequences(indi) #Secuencias de cada individuo
        apt= getFitnessInd(r,c,rS,cS)
        aptitudes.append(apt)
    
    return aptitudes


#Aptitud por individuo
def getFitnessInd(r,c,rowSequences,colSequences):
    f1 = sum(
        abs((r[i][j][0] - rowSequences[i][j][0]) if r[i][j][1] != rowSequences[i][j][1] else 0)  # Penalización por color, proporcional al tamaño de la secuencia
        for i in range(len(rowSequences))
        for j in range(len(rowSequences[0]))
    )
    f2= sum(
        abs((c[i][j][0] if c[i][j][1] != colSequences[i][j][1] else 0))  # Penalización por color, proporcional al tamaño de la secuencia
        for i in range(len(colSequences))
        for j in range(len(colSequences[0]))
    )
    aptitud=f1+f2
    return aptitud


#Secuencias por individuo
def getIndSequences(indiv): 
    rowSequences = []
    colSequences = []
    
    for i in range(len(indiv)):
        row = indiv[i]
        rowSeq = getColorSequence(row) #Secuencia de la fila
        rowSequences.append(rowSeq)

    for i in range(len(indiv[0])):    
        col = indiv[:, i] 
        colSeq = getColorSequence(col) #Secuencia de la columna
        colSequences.append(colSeq)
    
    return rowSequences,colSequences


#Secuencia de fila o columna
def getColorSequence(filaCol):
    sequence = []
    count = 0
    current_color = None
    
    for celda in filaCol:
        if celda != 0:  # Si la celda está pintada
            if celda == current_color:  # Si el color es el mismo, incrementa el contador
                count += 1
            else:  # Si cambia el color, guarda la secuencia anterior (si existe) y empieza una nueva
                if count > 0:
                    sequence.append((count, current_color))
                current_color = celda
                count = 1
        else:  # Si la celda está vacía
            if count > 0:
                sequence.append((count, current_color))
                count = 0
                current_color = None

    # Si queda una secuencia al final
    if count > 0:
        sequence.append((count, current_color))

    # Rellena con (0, 0) hasta alcanzar el tamano de la pista
    while len(sequence) < len(filaCol):
        sequence.insert(0, (0, 0))

    return sequence[-(len(filaCol)):]
