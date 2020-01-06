"""
--- Day 8: Space Image Format ---
The Elves' spirits are lifted when they realize you have an opportunity to reboot one of their Mars rovers, and so they are curious 
if you would spend a brief sojourn on Mars. You land your ship near the rover.

When you reach the rover, you discover that it's already in the process of rebooting! It's just waiting for someone to enter a BIOS password. 
The Elf responsible for the rover takes a picture of the password (your puzzle input) and sends it to you via the Digital Sending Network.

Unfortunately, images sent via the Digital Sending Network aren't encoded with any normal encoding; instead, they're encoded in a special Space 
Image Format. None of the Elves seem to remember why this is the case. They send you the instructions to decode it.

Images are sent as a series of digits that each represent the color of a single pixel. The digits fill each row of the image left-to-right, then move 
downward to the next row, filling rows top-to-bottom until every pixel of the image is filled.

Each image actually consists of a series of identically-sized layers that are filled in this way. So, the first digit corresponds to the top-left pixel 
of the first layer, the second digit corresponds to the pixel to the right of that on the same layer, and so on until the last digit, which corresponds 
the bottom-right pixel of the last layer.

For example, given an image 3 pixels wide and 2 pixels tall, the image data 123456789012 corresponds to the following image layers:

Layer 1: 123
         456

Layer 2: 789
         012
The image you received is 25 pixels wide and 6 pixels tall.

To make sure the image wasn't corrupted during transmission, the Elves would like you to find the layer that contains the fewest 0 digits. 
On that layer, what is the number of 1 digits multiplied by the number of 2 digits?
"""

from collections import Counter
import logging
LOG_FORMAT = "[%(levelname)s %(asctime)s] => %(message)s"
logging.basicConfig(level=logging.INFO,
                    format = LOG_FORMAT)

class Imagen(object):
    def __init__(self, datos, ancho=25, alto=6):
        self.datos = str(datos)
        self.capas = []
        self.ancho = ancho
        self.alto = alto
        self.long = self.ancho * self.alto
    
    def crear_capas(self):
        if not self.datos:            
            return        
        self.capas.append(list(map(int,self.datos[:self.long])))
        self.datos = self.datos[self.long:]
        logging.debug(f"CAPAS: {self.capas}, DATOS: {self.datos}")
        return self.crear_capas()
    
    def crear_contador_capas(self):
        self.contador = list(map(lambda capa: Counter(capa), self.capas))
    
    def obtener_contador_menor_cantidad(self, digito=0):
        self.contador.sort(key=lambda contador: contador[digito])
        return self.contador[0]

    def combinar_capas(self):                
        for i in range(len(self.capas[0])):            
            comb = []
            for capa in self.capas:
                comb.append(capa[i])
            yield comb

    def descodificar(self):
        def dame_primer_opaco(pixels):
            for pixel in pixels:
                if pixel == 0:
                    return " "
                elif pixel == 1:
                    return "*"
            return "t"        
        result = ""
        l = list(map(dame_primer_opaco, self.combinar_capas()))
        for _ in range(self.alto):
            result+=("".join(l[:self.ancho])+"\n")
            l = l[self.ancho:]        
        return result
        

if __name__ == "__main__":
    # ----- ----- ----- ----- ----- PARTE 1 ----- ----- ----- ----- ----- #

    path = "d:\\advent-of-code-2019\\day8\\"
    with open(path+"input.txt") as input:
        datos = input.read().strip()

    #datos = "0222112222120000"    

    imagen = Imagen(datos, 25, 6)
    imagen.crear_capas()
    imagen.crear_contador_capas()

    contador = imagen.obtener_contador_menor_cantidad()
    print(contador[1]*contador[2])

    # ----- ----- ----- ----- ----- PARTE 1 ----- ----- ----- ----- ----- #

    print(imagen.descodificar())


