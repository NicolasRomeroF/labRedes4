import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import read,write
from scipy.interpolate import interp1d

'''
Funcion que lee el archivo de entrada y retorna la señal junto con su tasa de muestreo
'''
def abrirArchivo():
    rate,info = read("handel.wav")
    print("El rate del archivo es: " + str(rate))
	#print(info)

    dimension = info[0].size
	#print(dimension)  

    if dimension == 1:
    	data = info
    	perfect = 1
    else:
    	data = info[:,dimension-1]

    return data,rate

def modulacion_ASK (x,bp):
    A1 = 1
    A2 = 0
    br = 1/bp    #frecuencia de bit
    f = br*10
    t2 = np.arange(bp/100,bp+bp/100,bp/1000)
    m=[]

    for i in range(len(x)):
        if x[i] == 1:
            y = A1*np.cos(2*np.pi*f*t2)
        else:
            y = A2*np.cos(2*np.pi*f*t2)
        m=np.concatenate((m,y))
    return m,t2

'''
Funcion que grafica los datos entregados.
'''
def graficar(title,xlabel,ylabel,X,Y):
    print("Mostrando grafico")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.plot(X, Y, "-")
    plt.show()

def interpolacion(data,rate):
    tiempo = np.linspace(0,len(data)/rate, num=len(data))
    interp = interp1d(tiempo,data)
    tiempo2 = np.linspace(0,len(data)/rate,len(data)*1000)
    y = interp(tiempo2)
    #print (tiempo[-1])
    #print(len(data)/rate)
    return y

def binarioTransform(info):
    l = []
    for i in info:
        binario = bin(i)[2:]
        if binario[0]=='b':
            i=i*-1
            binario = bin(i)[2:]
        l.append(binario)
    maxLen = max(l, key=len)
    lf = []
    for dato in l:
        lf.append(dato.zfill(len(maxLen)))
    return lf

x = [0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1]

data,rate = abrirArchivo()
m,t = modulacion_ASK(x,1)
print(data)

binData = binarioTransform(data)
index = int(np.ceil((10**5)/len(binData[0])))
binData = binData[:index]
print("index: " +str(index))

print(binData)
print(len(binData))
#graficar("Señal modulada","Amplitud","Tiempo",x,y)