import tkinter as tk

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
        color = "black" if bit == "1" else ("white" if bit == "0" else "gray")
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
    mostrarBits(mensajeBinario, segundaVentana, 1, 2)
 
    botonContinuar = tk.Button(segundaVentana, text="Ver mensaje resultante", command=lambda:[segundaVentana.destroy(), crearVentanaResultado("Aún no modificar esta parte, falta correcion Hamming")])
    botonContinuar.grid(columnspan=2, pady=10, padx=10)

def crearVentanaResultado(mensajeDesencriptado):
    terceraVentana = tk.Toplevel(menu)
    terceraVentana.title("Mensaje Desencriptado")

    tk.Label(terceraVentana, text="El texto que encriptaste y que ha sido desencriptado es el siguiente: ").grid(row=0,column=0, pady=10, padx=10)
    tk.Label(terceraVentana, text=mensajeDesencriptado).grid(row=0,column=1, padx=10, pady=10)

    botonCerrar = tk.Button(terceraVentana, text="Cerrar/Volver al menú principal", command=terceraVentana.destroy)
    botonCerrar.grid(row=1, columnspan=2, pady=10, padx=10)
    

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