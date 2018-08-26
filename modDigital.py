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

'''Funcion que devuelve un vector de ruidos de tamaño N
   Entrada: tamaño del vector de ruidos, signal noise ratio
   Salida: vector de ruidos
'''
def agregarRuido(N, SNR):
    ruido = np.random.normal(0.0, 1.0/SNR, N)
    return ruido

'''Funcion que modula un vector de bits x con tiempo de bit bp
   Entrada: vector de bits, tiempo de bit
   Salida: señal modulada
'''
def modulacion_ASK (x,bp):
    A1 = 1
    A2 = 0
    br = 1/bp    #frecuencia de bit
    f = br*10
    t2 = np.arange(bp/100,bp+bp/100,bp/100)
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

'''Funcion que transforma los datos a binario
   Entrada: vector de datos
   Salida: vector de datos en binario (lista de strings)
'''
def binarioTransform(data):
    l = []
    for i in data:
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

'''Funcion que tansforma la lista de binarios en string a lista de bits int
   Entrada: datos en binario
   Salida: lista de bits
'''
def binary_flat(data):
    largo = len(data[0])
    flat = []
    for i in range(len(data)):
        for j in range(largo):
            flat.append(int(data[i][j]))
    return flat

'''Funcion que demodula una señal
   Entrada: Señal modulada, vector de tiempo, tiempo de bit
   Salida: señal demodulada
'''
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

'''Funcion que extiende los bits para simular una señal cuadrada
    Entrada: vecto de datos
    Salida: señal cuadrada
'''
def squareSignal(data):
    t2 = np.ones((100))
    m=[]

    for i in range(len(data)):
        if data[i] == 1:
            y = t2
        else:
            y = 0*t2
        m=np.concatenate((m,y))
    return m

'''Funcion que contabiliza la cantidad de errores de una señal ruidosa
   Entrada: señal demodulada sin ruido, señal demodulada con ruido
   Salida: tasa de error
'''
def cant_error(demodulada,demoduladaRuido):
    error = 0
    for i in range(len(demodulada)):
        if demodulada[i] != demoduladaRuido[i]:
            error += 1
    return error
    

#BLOQUE PRINCIPAL
try:
    data,rate = abrirArchivo()
except:
    print("Error al abrir el archivo")
    exit(1)


binData = binarioTransform(data)

cantBits = int(input("Ingrese la cantidad de bits con la que quiere trabajar\n(Valores mayores de 10000 hacen que el programa demore mas): "))
tiempoBit = float(input("Ingrese tiempo de bit: "))
index = int(np.ceil((cantBits)/len(binData[0])))

binData = binData[:index]

flat = binary_flat(binData)
bp = tiempoBit
square = squareSignal(flat)
modulada,tb = modulacion_ASK(flat,bp)
t = np.arange(bp/100,(bp)*len(flat)+bp/200,bp/100)
N = len(modulada)

demodulada=demodulacion_ASK(modulada,tb,bp)

SNRs = [2.0, 4.0, 6.0, 8.0, 10.0]
errores = []
size = len(flat)
for snr in SNRs:
    moduladaRuido = modulada+agregarRuido(N,snr)
    demoduladaRuido = demodulacion_ASK(moduladaRuido,tb,bp)
    error = (cant_error(demodulada,demoduladaRuido)/cantBits)*100
    errores.append(error)


squareDemodulada = squareSignal(demodulada)



opcion=1
while opcion != 0:
    print("""Menú:
    1.- Mostrar audio digital
    2.- Mostrar señal modulada
    3.- Mostrar señal demodulada
    4.- Tasa de errores segun SNR (2, 4, 6, 8, 10)

    5.- Salir""")
    try:
        opcion = int(input("Ingrese una opción: "))
    except:
        opcion = 6
    if opcion==1:
        graficar("Audio","Tiempo [s]","Valor",t,square)
    elif opcion==2:
        graficar("Audio","Tiempo [s]","Amplitud",t,modulada)
    elif opcion==3:
        graficar("Audio","Tiempo [s]","Valor",t,squareDemodulada)
    elif opcion==4:
        graficar("Tasa de errores segun SNR","SNR","Tasa de error (%)",SNRs,errores)

    elif opcion == 5:
        opcion = 0
        print("Salir")
#print(flat)
#graficar("Señal modulada","Tiempo","Amplitud",t,modulada)