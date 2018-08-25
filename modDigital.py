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

def agregarRuido(N, SNR):
    ruido = np.random.normal(0.0, 1.0/SNR, N)
    return ruido


def modulacion_ASK (x,bp):
    A1 = 1
    A2 = 0
    br = 1/bp    #frecuencia de bit
    f = br*10
    t2 = np.arange(bp/100,bp+bp/1000,bp/100)
    m=[]
    tb = len(t2)

    for i in range(len(x)):
        if x[i] == 1:
            y = A1*np.cos(2*np.pi*f*t2)
        else:
            y = A2*np.cos(2*np.pi*f*t2)
        m=np.concatenate((m,y))
    return m,tb

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

def binarioTransform(data):
    l = []
    for i in data:
        #print(bin(i))
        binario = bin(i)[2:]
        if binario[0]=='b':
            i=i*-1
            binario = "1"+bin(i)[2:]
        else:
            binario = "0" + binario
        l.append(binario)
    maxLen = max(l, key=len)
    lf = []
    for dato in l:
        lf.append(dato.zfill(len(maxLen)))
    return lf

def binary_flat(data):
    largo = len(data[0])
    flat = []
    for i in range(len(data)):
        for j in range(largo):
            flat.append(int(data[i][j]))
    return flat

def demodulacion_ASK(modulada,tb,bp):
    mn=[]
    f=10/bp
    for n in range(tb,len(modulada)+tb,tb):
        t=np.arange(bp/100,bp,bp/100)
        y=np.cos(2*np.pi*f*t)                                       
        mm=np.multiply(y,modulada[n-(tb-1):n])
        t4=np.arange(bp/100,bp,bp/100)
        z=np.trapz(t4,mm)                                              
        zz=np.round((2*z/bp))                                     
        if(zz>=1.0):                     
            a=1
        else:
            a=0
        mn.append(a)
    return mn
    

x = [0,1,0,0,1,0,1,1,1,0,1,0,1,0,1,0,1]

data,rate = abrirArchivo()
print(data)

binData = binarioTransform(data)
index = int(np.ceil((10**2)/len(binData[0])))
binData = binData[:index]

flat = binary_flat(binData)
bp = 2
modulada,tb = modulacion_ASK(flat,bp)
t = np.arange(bp/100,(bp)*len(flat)+bp/100,bp/100)
N = len(modulada)
SNR = 5.0
ruido = agregarRuido(N,SNR)
senalRuido = modulada + ruido
#print(len(flat))
print(demodulacion_ASK(modulada,tb,bp))
print(demodulacion_ASK(senalRuido,tb,bp))
#print(flat)
#graficar("Señal modulada","Tiempo","Amplitud",t,modulada)