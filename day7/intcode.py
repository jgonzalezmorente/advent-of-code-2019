class IntCode(object):
    def __init__(self, programa, entradas=[], saltar=True):
        self.programa = programa        
        self.entradas = entradas
        self.salidas = []        
        self.texto_error = "El programa introducido como entrada no es válido."
        self.puntero = 0
        self.saltar = saltar
        self.programa_finalizado = False

    def ejecutar_programa(self):        
        instruccion = "{:05d}".format(self.programa[self.puntero])        
        opcode = int(instruccion[-2:])
        modo1 = int(instruccion[-3])
        modo2 = int(instruccion[-4])
        modo3 = int(instruccion[-5])
        if ( (not opcode in [1, 2, 3, 4, 5, 6, 7, 8, 99]) 
          or (not {modo1, modo2, modo3}.issubset({0, 1})) ):
            raise ValueError(self.texto_error)
        try:
            if opcode == 99:
                self.puntero+=1
                self.programa_finalizado = True
                return
            elif opcode == 1 or opcode == 2:
                operacion = (lambda x, y: x+y) if opcode == 1 else (lambda x, y: x*y)
                self.programa[self.programa[self.puntero+3]] = operacion(self.obtener_valor(modo1, self.puntero+1), self.obtener_valor(modo2, self.puntero+2))
                self.puntero+=4
                return self.ejecutar_programa()    
            elif opcode == 3:
                if self.entradas:
                    self.programa[self.programa[self.puntero+1]] = self.entradas.pop()
                    self.puntero+=2
                    return self.ejecutar_programa()
                else:                    
                    raise ValueError(self.texto_error)
            elif opcode == 4:                
                self.salidas.append(self.obtener_valor(modo1, self.puntero+1))
                self.puntero+=2
                if self.saltar:
                    return
                self.entradas.insert(0, self.salidas[-1])
                return self.ejecutar_programa()
            elif opcode == 5 or opcode == 6:
                if (opcode == 5 and self.obtener_valor(modo1, self.puntero+1) != 0) or (opcode == 6 and self.obtener_valor(modo1, self.puntero+1) == 0):
                    self.puntero = self.obtener_valor(modo2, self.puntero+2)
                else:
                    self.puntero+=3
                return self.ejecutar_programa()
            elif opcode == 7 or opcode == 8:
                if ((opcode == 7 and (self.obtener_valor(modo1, self.puntero+1) < self.obtener_valor(modo2, self.puntero+2))) 
                  or (opcode == 8 and (self.obtener_valor(modo1, self.puntero+1) == self.obtener_valor(modo2, self.puntero+2)))):
                    self.programa[self.programa[self.puntero+3]] = 1
                else:
                    self.programa[self.programa[self.puntero+3]] = 0
                self.puntero+=4
                return self.ejecutar_programa()
        except:
            raise ValueError(self.texto_error)

    def obtener_valor(self, modo, puntero):
        if modo == 0:
            return self.programa[self.programa[puntero]]
        else:
            return self.programa[puntero]