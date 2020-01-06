class IntCode(object):
    def __init__(self, programa):
        self.programa = programa
        self.codigo_diagnostico = None
        self.salidas = []

    def ejecutar_programa(self, i=0, input=None):
        instruccion = "{:05d}".format(self.programa[i])
        texto_error = f"El programa introducido como entrada no es válido. Instrucción {instruccion} incorrecta."
        opcode = int(instruccion[-2:])
        modo1 = int(instruccion[-3])
        modo2 = int(instruccion[-4])
        modo3 = int(instruccion[-5])

        if ( (not opcode in [1, 2, 3, 4, 5, 6, 7, 8, 99]) 
          or (not {modo1, modo2, modo3}.issubset({0, 1}))
          or (opcode == 3 and input==None) ):
            raise ValueError(texto_error)

        try:
            if opcode == 99:
                return

            elif opcode == 1 or opcode == 2:
                operacion = (lambda x, y: x+y) if opcode == 1 else (lambda x, y: x*y)
                self.programa[self.programa[i+3]] = operacion(self.obtener_valor(modo1, i+1), self.obtener_valor(modo2, i+2))
                return self.ejecutar_programa(i=i+4)
    
            elif opcode == 3:
                self.programa[self.programa[i+1]] = input
                return self.ejecutar_programa(i=i+2)

            elif opcode == 4:
                self.codigo_diagnostico = self.obtener_valor(modo1, i+1)
                self.salidas.append(self.codigo_diagnostico)
                return self.ejecutar_programa(i=i+2, input=self.codigo_diagnostico)

            elif opcode == 5 or opcode == 6:
                if (opcode == 5 and self.obtener_valor(modo1, i+1) != 0) or (opcode == 6 and self.obtener_valor(modo1, i+1) == 0):
                    puntero = self.obtener_valor(modo2, i+2)
                else:
                    puntero = i+3
                return self.ejecutar_programa(i=puntero)

            elif opcode == 7 or opcode == 8:
                if ((opcode == 7 and (self.obtener_valor(modo1, i+1) < self.obtener_valor(modo2, i+2))) 
                  or (opcode == 8 and (self.obtener_valor(modo1, i+1) == self.obtener_valor(modo2, i+2)))):
                    self.programa[self.programa[i+3]] = 1
                else:
                    self.programa[self.programa[i+3]] = 0
                return self.ejecutar_programa(i=i+4)

        except:
            raise ValueError(texto_error)

    def obtener_valor(self, modo, puntero):
        if modo == 0:
            return self.programa[self.programa[puntero]]
        else:
            return self.programa[puntero]