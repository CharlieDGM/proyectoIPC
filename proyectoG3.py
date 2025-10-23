import tkinter as tk
import random

#####################################
#FUNCIONES para convertir el string encriptado con ROT13 a binario y viceversa
def ROT13toBit(texto_de_entrada):
    bit_de_salida = ' '.join(format(ord(c), '08b') for c in texto_de_entrada)
    return bit_de_salida

def BitToROT13(bit_de_entrada):
    chars = bit_de_entrada.split()
    texto_original = ''.join(chr(int(b, 2)) for b in chars)
    return texto_original

####################################
#FUNCIONES para encriptar el string con ROT13
def StringToROT13(texto):
    resultado = ""
    for c in texto:
        if 'a' <= c <= 'z':
            resultado += chr((ord(c) - ord('a') + 13) % 26 + ord('a'))
        elif 'A' <= c <= 'Z':
            resultado += chr((ord(c) - ord('A') + 13) % 26 + ord('A'))
        else:
            resultado += c
    return resultado

def ROT13ToString(texto):
    return StringToROT13(texto)
#########################################
#FUNCIONES PARA CODIGO HAMMING
#Vamos a recibir un string con grupos de 8 bits cada uno, cada uno representando una letra, necesitamos dividir el string en grupos de 8 y luego convertir cada grupo a codigos hamming

def codificacionHamming(bitsEntrada):
    bitsEntrada = list(map(int, bitsEntrada))
    h = [0] * 13

    h[3], h[5], h[6], h[7], h[9], h[10], h[11], h[12] = bitsEntrada

    #bits de paridad
    h[1] = (h[3] ^ h[5] ^ h[7] ^ h[9] ^ h[11]) 
    h[2] = (h[3] ^ h[6] ^ h[7] ^ h[10] ^ h[11])
    h[4] = (h[5] ^ h[6] ^ h[7] ^ h[12]) 
    h[8] = (h[9] ^ h[10] ^ h[11] ^ h[12]) 
    
    return ''.join(str(bit) for bit in h[1:])

def decodificacionHamming(bitsEntrada):
    h = [0] + list(map(int, bitsEntrada))

    c1 = (h[1] ^ h[3] ^ h[5] ^ h[7] ^ h[9] ^ h[11]) 
    c2 = (h[2] ^ h[3] ^ h[6] ^ h[7] ^ h[10] ^ h[11])
    c4 = (h[4] ^ h[5] ^ h[6] ^ h[7] ^ h[12]) 
    c8 = (h[8] ^ h[9] ^ h[10] ^ h[11] ^ h[12]) 

    posError = c1 + 2*c2 + 4*c4 + 8*c8

    if posError != 0:
        h[posError] = h[posError] ^ 1

    bitsOriginales = [h[3], h[5], h[6], h[7], h[9], h[10], h[11], h[12]]

    bitsHammCorrectos = ''.join(str(bit) for bit in h[1:])
    bitsOriginales = ''.join(str(bit) for bit in bitsOriginales)

    return bitsHammCorrectos, bitsOriginales, posError

def errorAleatorio(bitsEntrada):
    bitsEntrada = list(map(int, bitsEntrada))
    posAleatoria = random.randint(0, 12)
    bitsEntrada[posAleatoria] = bitsEntrada[posAleatoria] ^ 1

    bitsEntrada = ''.join(str(bit) for bit in bitsEntrada)
    return bitsEntrada

def BitToHamming(stringEntrada):
    grupos = stringEntrada.split()
    bitsHammingCorrectos = []
    bitsHammingIncorrectos = []

    for grupo in grupos:
        bitsHammingCorrectos.append(codificacionHamming(grupo))

    bitsHammingCorrectos = ' '.join(bitsHammingCorrectos)

    for grupo in grupos:
        bitsHammingIncorrectos.append(errorAleatorio(codificacionHamming(grupo)))

    bitsHammingIncorrectos = ' '.join(bitsHammingIncorrectos)
    
    return bitsHammingCorrectos, bitsHammingIncorrectos


######################################
#FUNCIONES GUI
def mostrarBits(cadenaBits, contenedor, fila, columna):
    anchoCuadro = 15
    altoCuadro = 15
    anchoTotal = len(cadenaBits) * anchoCuadro

    canva = tk.Canvas(contenedor, width=anchoTotal, height=altoCuadro)
    canva.grid(row=fila, column=columna, pady=10, padx=10)

    for i, bit in enumerate(cadenaBits):
        coordenadaInicial = i * anchoCuadro
        coordenadaFinal = coordenadaInicial + anchoCuadro
        color = "black" if bit == "1" else ("white" if bit == "0" else "blue")
        canva.create_rectangle(coordenadaInicial, 0, coordenadaFinal, altoCuadro, fill=color, outline="gray")
    #esto crea un rectangulo con "i" cantidad de cuadros, donde cada cuadro esta formado por las puntos (coordenadaFinal, 0) y (coordeanadaFinal, altoCuadro)

def crearVentanaVisualizacion():
    mensajeOriginal = inputMensaje.get()
    mensajeCifrado = StringToROT13(mensajeOriginal)

    segundaVentana = tk.Toplevel(menu)
    segundaVentana.title("Proceso de encriptación paso a paso")

    tk.Label(segundaVentana, text="Mensaje encriptado con ROT13: ").grid(row=0, column=0, pady=10, padx=10)
    tk.Label(segundaVentana, text=mensajeCifrado).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(segundaVentana, text="Mensaje encriptado a binario: ").grid(row=1, column=0, padx=10, pady=10)
    mensajeBinario = ROT13toBit(mensajeCifrado)
    mostrarBits(mensajeBinario, segundaVentana, 1, 1)

    ######
    #DECLARAR VARIABLES para almacenar los strings de ambos codigos cifrados con hamming
    c, i = BitToHamming(mensajeBinario)
    tk.Label(segundaVentana, text="Mensaje cifrado con Hamming (correcto, sin errores): ").grid(row=2, column=0, padx=10, pady=10)
    mostrarBits(c, segundaVentana, 2, 1)
    tk.Label(segundaVentana, text="Mensaje cifrado con Hamming (con un error en cada grupo de bits): ").grid(row=3, column=0, padx=10, pady=10)
    mostrarBits(i, segundaVentana, 3, 1)
    
    botonContinuar = tk.Button(segundaVentana, text="Ver mensaje resultante", command=lambda:[segundaVentana.destroy(), crearVentanaResultado(i)])
    botonContinuar.grid(columnspan=2, pady=10, padx=10)

def crearVentanaResultado(bitsIncorrectos):
    terceraVentana = tk.Toplevel(menu)
    terceraVentana.title("Mensaje Desencriptado")

    tk.Label(terceraVentana, text="Los bits incorrectos con Hamming eran: ").grid(row=0, column=0, pady=10, padx=10)
    mostrarBits(bitsIncorrectos, terceraVentana, 0, 1)

    grupos = bitsIncorrectos.split()
    bitsHammCorrectos = []
    bitsOriginales = []
    posicionesErroes = []

    for grupo in grupos:
        c, o, e = decodificacionHamming(grupo)
        bitsHammCorrectos.append(c)
        bitsOriginales.append(o)
        posicionesErroes.append(e)

    bitsHammCorrectos = ' '.join(bitsHammCorrectos)
    bitsOriginales = ' '.join(bitsOriginales)

    tk.Label(terceraVentana, text="Los bits corregidos con el codigo hamming son: ").grid(row=1, column=0, padx=10, pady=10)
    mostrarBits(bitsHammCorrectos, terceraVentana, 1, 1)
    tk.Label(terceraVentana, text="Los bits encriptados originales eran: ").grid(row=2, column=0, padx=10, pady=10)
    mostrarBits(bitsOriginales, terceraVentana, 2, 1)
    tk.Label(terceraVentana, text="Las posiciones de los bits incorrectos eran: ").grid(row=3, column=0, padx=10, pady=10)
    tk.Label(terceraVentana, text=str(posicionesErroes)).grid(row=3, column=1, padx=10, pady=10)

    tk.Label(terceraVentana, text="Procederemos a aplicar los pasos inversos para obtener el mensaje original").grid(row=4, columnspan=2, padx=10, pady=10)

    mensajeROT13 = BitToROT13(bitsOriginales)
    mensajeOriginal = ROT13ToString(mensajeROT13)
    tk.Label(terceraVentana, text="El mensaje original era: ").grid(row=5, column=0, padx=10, pady=10)
    tk.Label(terceraVentana, text=mensajeOriginal).grid(row=5, column=1, padx=10, pady=10)

    botonCerrar = tk.Button(terceraVentana, text="Cerrar/Volver al menú principal", command=terceraVentana.destroy)
    botonCerrar.grid(columnspan=2, pady=10, padx=10)
    

menu = tk.Tk()
menu.title("Sistema de encriptación - IPC G#3")
menu.grid_rowconfigure(0, weight=1)
menu.grid_columnconfigure(0, weight=1)

tk.Label(menu, text="Sistema de encriptacion avanzado yeah").grid(row=0,columnspan=2, pady=10)
inputMensaje = tk.Entry(menu)
tk.Label(menu, text="Ingresa el mensaje que deseas encriptar y mandar: ").grid(row=1,column=0, padx=10)
inputMensaje.grid(row=1,column=1, padx=10)
boton = tk.Button(menu, text="Encriptar mensaje",command=crearVentanaVisualizacion)
boton.grid(row=2, pady=10, columnspan=2)

menu.mainloop()