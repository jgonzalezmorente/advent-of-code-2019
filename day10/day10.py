#%%
import copy
from functools import total_ordering
# %%
class Punto(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.detectado = False
        self.numero_detecciones = 0       
    
    def esIgual(self, punto):
        if self.x == punto.x and self.y == punto.y:
            return True
        else:
            return False
    
    def vector(self, punto):
        return (punto.x - self.x, punto.y - self.y)
    
    def distancia(self, punto):
        v = self.vector(punto)
        return (v[0]**2 + v[1]**2)

    def __str__(self):
        return f'({self.x}, {self.y}), {self.numero_detecciones}'
#%%
@total_ordering
class LineaVision(object):
    puntoOrigen = None
    
    def __init__(self):
        self.puntos = []
        self.vector_ = None
        
    def addPunto(self, punto):
        self.puntos.append(punto)
    
    def ordenar(self):
        self.puntos.sort(key=lambda x: LineaVision.puntoOrigen.distancia(x))
    
    def vector(self):
        if self.puntos:
            self.vector_ = LineaVision.puntoOrigen.vector(self.puntos[0])
            return self.vector_
    
    def determinante(self, lineaVision):
        if not self.vector_:
            self.vector()
        if not lineaVision.vector_:
            lineaVision.vector()
        return (self.vector_[0]*lineaVision.vector_[1]-self.vector_[1]*lineaVision.vector_[0])
    
    def cuadrante(self):
        if not self.vector_:
            self.vector()
        if self.vector_[0] >= 0 and self.vector_[1] >= 0:
            return 1
        elif self.vector_[0] >= 0 and self.vector_[1] < 0:
            return 2
        elif self.vector_[0] < 0 and self.vector_[1] <= 0:
            return 3
        elif self.vector_[0] < 0 and self.vector_[1] > 0:
            return 4

    def __eq__(self, other):
        if self.cuadrante() == other.cuadrante() and self.determinante(other) == 0:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)        

    def __lt__(self, other):
        if self.cuadrante() < other.cuadrante():
            return True
        elif self.cuadrante() == other.cuadrante():
            if self.determinante(other) < 0:
                return True
            else:
                return False
        else:
            return False
    
# %%
path = "d:\\advent-of-code-2019\\day10\\"
with open(path+"input.txt") as input:
    datos = input.readlines()

mapa = []
for j, fila in enumerate(datos):
    for i, d in enumerate(fila):
        if d == '#':            
            mapa.append(Punto(i, -j))

# %%
for origen in mapa:
    mapa_c = [copy.copy(p) for p in mapa]
    for destino in mapa_c:
        if not origen.esIgual(destino) and not destino.detectado:
            suma = 1
            v_origen = origen.vector(destino)
            for a in mapa_c:
                if not origen.esIgual(a) and not a.detectado:
                    v_a = origen.vector(a)
                    det = (v_origen[0] * v_a[1]) - (v_origen[1] * v_a[0])
                    if det == 0:                        
                        a.detectado = True
                        if v_a[0]*v_origen[0] <= 0 and v_a[1]*v_origen[1] <= 0:
                            suma = 2
            origen.numero_detecciones += suma 
# %%
mapa.sort(key=lambda x: x.numero_detecciones)
print(mapa[-1])
# %%
mapa_c = [copy.copy(p) for p in mapa]

lineasVision = []

LineaVision.puntoOrigen = mapa[-1]
for destino in mapa_c:
    if not LineaVision.puntoOrigen.esIgual(destino) and not destino.detectado:
        lineaVision = LineaVision()
        lineasVision.append(lineaVision)
        lineaVision.addPunto(destino)
        vectorOrigen = lineaVision.vector()
        
        for a in mapa_c:
            if (not LineaVision.puntoOrigen.esIgual(a) 
                and not destino.esIgual(a) and not a.detectado):
                    
                vector_a = LineaVision.puntoOrigen.vector(a)
                determinante = (vectorOrigen[0]*vector_a[1] - vectorOrigen[1]*vector_a[0])
                if determinante == 0:
                    productoEscalar = vectorOrigen[0]*vector_a[0] + vectorOrigen[1]*vector_a[1]
                    if productoEscalar > 0:
                        a.detectado = True
                        lineaVision.addPunto(a)
        
        lineaVision.ordenar()
#%%
lineasVision.sort()
#%%

contador = 0
while(contador<200):
    for lineaVision in lineasVision:
        if lineaVision.puntos:
            asteroide = lineaVision.puntos.pop(0)
            contador += 1
            print(contador, asteroide)            
            if contador == 200:
                break
            

#%%
print(asteroide.x * 100 - asteroide.y)
print(asteroide)