class IntCode(object):
    def __init__(self, programa, entradas=[], saltar=True):
        self.programa = programa        
        self.entradas = entradas
        self.salidas = []        
        self.texto_error = "El programa introducido como entrada no es válido."
        self.puntero = 0
        self.base_relativa = 0
        self.saltar = saltar
        self.programa_finalizado = False
        self.long_programa = len(self.programa)
        self.iter = 0

    def ejecutar_programa(self, recursivo=True):
        while(not self.programa_finalizado):
            self.iter += 1
            instruccion = "{:05d}".format(self.programa[self.puntero])        
            opcode = int(instruccion[-2:])
            modo1 = int(instruccion[-3])
            modo2 = int(instruccion[-4])
            modo3 = int(instruccion[-5])        
            if ( (not opcode in [1, 2, 3, 4, 5, 6, 7, 8, 9, 99]) 
            or (not {modo1, modo2, modo3}.issubset({0, 1, 2})) ):
                raise ValueError(self.texto_error)
            try:
                if opcode == 99:
                    self.puntero+=1
                    self.programa_finalizado = True
                    return
                elif opcode == 1 or opcode == 2:
                    operacion = (lambda x, y: x+y) if opcode == 1 else (lambda x, y: x*y)
                    self.puntero+=1
                    valor1 = self.obtener_valor(modo1)
                    self.puntero+=1
                    valor2 = self.obtener_valor(modo2)
                    self.puntero+=1
                    self.escribir_valor(operacion(valor1, valor2), self.obtener_valor(1) + self.base_relativa if modo3==2 else self.obtener_valor(1))
                    self.puntero+=1
                    if recursivo:
                        return self.ejecutar_programa()    
                elif opcode == 3:
                    if self.entradas:
                        self.puntero+=1
                        self.escribir_valor(self.entradas.pop(), self.obtener_valor(1) + self.base_relativa if modo1==2 else self.obtener_valor(1))
                        self.puntero+=1
                        if recursivo:
                            return self.ejecutar_programa()
                    else:                    
                        raise ValueError(self.texto_error)
                elif opcode == 4:
                    self.puntero+=1
                    self.salidas.append(self.obtener_valor(modo1))
                    self.puntero+=1
                    if self.saltar:
                        return
                    self.entradas.insert(0, self.salidas[-1])
                    if recursivo:
                        return self.ejecutar_programa()
                elif opcode == 5 or opcode == 6:
                    self.puntero+=1 
                    valor = self.obtener_valor(modo1)
                    self.puntero+=1
                    if (opcode == 5 and valor != 0) or (opcode == 6 and valor == 0):                    
                        self.puntero = self.obtener_valor(modo2)
                    else:
                        self.puntero+=1
                    if recursivo:
                        return self.ejecutar_programa()
                elif opcode == 7 or opcode == 8:
                    self.puntero+=1
                    valor1 = self.obtener_valor(modo1)
                    self.puntero+=1
                    valor2 = self.obtener_valor(modo2)                
                    self.puntero+=1
                    if ((opcode == 7 and (valor1 < valor2)) 
                    or (opcode == 8 and (valor1 == valor2))):                  
                        self.escribir_valor(1, self.obtener_valor(1) + self.base_relativa if modo3==2 else self.obtener_valor(1))
                    else:
                        self.escribir_valor(0, self.obtener_valor(1) + self.base_relativa if modo3==2 else self.obtener_valor(1))
                    self.puntero+=1
                    if recursivo:
                        return self.ejecutar_programa()
                elif opcode == 9:
                    self.puntero+=1
                    self.base_relativa+=self.obtener_valor(modo1)
                    self.puntero+=1
                    if recursivo:
                        return self.ejecutar_programa()
                if recursivo:
                    break
            except:            
                raise ValueError(self.texto_error)

    def obtener_valor(self, modo):
        if modo == 0:
            valor = self.obtener_valor(1)
            self.aumentar_memoria(valor)
            return self.programa[valor]
        elif modo == 1:
            self.aumentar_memoria()
            return self.programa[self.puntero]        
        elif modo == 2:
            valor = self.obtener_valor(1) + self.base_relativa
            self.aumentar_memoria(valor)
            return self.programa[valor]        
    
    def aumentar_memoria(self, posicion=None):
        n = posicion if posicion else self.puntero
        if n >= self.long_programa:
            incremento = n - self.long_programa + 1
            for _ in range(incremento):
                self.programa.append(0)

    def escribir_valor(self, valor, posicion):
        self.aumentar_memoria(posicion)        
        self.programa[posicion] = valor



