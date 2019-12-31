"""
--- Day 6: Universal Orbit Map ---
You've landed at the Universal Orbit Map facility on Mercury. Because navigation in space often 
involves transferring between orbits, the orbit maps here are useful for finding efficient routes 
between, for example, you and Santa. You download a map of the local orbits (your puzzle input).

Except for the universal Center of Mass (COM), every object in space is in orbit around exactly 
one other object. An orbit looks roughly like this:

                  \
                   \
                    |
                    |
AAA--> o            o <--BBB
                    |
                    |
                   /
                  /
In this diagram, the object BBB is in orbit around AAA. The path that BBB takes around AAA 
(drawn with lines) is only partly shown. In the map data, this orbital relationship is written AAA)BBB, 
which means "BBB is in orbit around AAA".

Before you use your map data to plot a course, you need to make sure it wasn't corrupted during 
the download. To verify maps, the Universal Orbit Map facility uses orbit count checksums - the total 
number of direct orbits (like the one shown above) and indirect orbits.

Whenever A orbits B and B orbits C, then A indirectly orbits C. This chain can be any number of 
objects long: if A orbits B, B orbits C, and C orbits D, then A indirectly orbits D.

For example, suppose you have the following map:

COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
Visually, the above map of orbits looks like this:

        G - H       J - K - L
       /           /
COM - B - C - D - E - F
               \
                I
In this visual representation, when two objects are connected by a line, the one on the right directly 
orbits the one on the left.

Here, we can count the total number of orbits as follows:

D directly orbits C and indirectly orbits B and COM, a total of 3 orbits.
L directly orbits K and indirectly orbits J, E, D, C, B, and COM, a total of 7 orbits.
COM orbits nothing.
The total number of direct and indirect orbits in this example is 42.

What is the total number of direct and indirect orbits in your map data?
"""

#%%

class Mapa(object):
    def __init__(self, orbitas):
        self.orbitas = [tuple(orb.split(')')) for orb in orbitas]
        self.contador_orbitas = []
        self.rutas_orbitas = []
        
    def extraer_objetos(self):
        self.objetos_ = set()
        for orb in self.orbitas:
            self.objetos_.add(orb[0])
            self.objetos_.add(orb[1])
    
    def buscar_contador_cache(self, objeto):
        for cont_orb in self.contador_orbitas:
            if cont_orb[0] == objeto:
                return cont_orb[1]
        return None

    def buscar_ruta_orbita_cache(self, objeto):
        for ruta in self.rutas_orbitas:
            if ruta[0] == objeto:                
                return ruta[1]
            elif objeto in ruta[1]:
                return ruta[1][ruta[1].index(objeto)+1:]
        return None
    
    def buscar_orbita_directa(self, objeto):        
        for orb in self.orbitas:
            if orb[1] == objeto:
                return orb[0]
        return None                

    def cuenta_orbitas(self, objeto, objeto_inicial=None, contador_actual=0):
        if not objeto_inicial:
            objeto_inicial = objeto

        result_cache = self.buscar_contador_cache(objeto)
        if result_cache:
            contador_actualizado = result_cache + contador_actual
            self.contador_orbitas.append((objeto_inicial, contador_actualizado))
            return contador_actualizado

        orb_directa = self.buscar_orbita_directa(objeto)
        if not orb_directa:
            self.contador_orbitas.append((objeto_inicial, contador_actual))
            return contador_actual
        else:            
            return self.cuenta_orbitas(orb_directa, objeto_inicial, contador_actual + 1)
    
    def cuenta_orbitas_total(self):
        total_orbitas = 0
        for obj in self.objetos_:
            total_orbitas += self.cuenta_orbitas(obj)
        return total_orbitas
    
    def obtener_ruta_orbita(self, objeto, objeto_inicial=None, p_ruta=[]):
        if not objeto_inicial:
            objeto_inicial = objeto
        
        ruta_cache = self.buscar_ruta_orbita_cache(objeto)
        if ruta_cache:
            ruta = p_ruta + ruta_cache                      
            if not (objeto_inicial, ruta) in self.rutas_orbitas:
                self.rutas_orbitas.append((objeto_inicial, ruta))
            return ruta
        
        orb_directa = self.buscar_orbita_directa(objeto)
        if not orb_directa:
            self.rutas_orbitas.append((objeto_inicial, p_ruta))
            return p_ruta
        else:            
            ruta = p_ruta.copy()
            ruta.append(orb_directa)
            return self.obtener_ruta_orbita(orb_directa, objeto_inicial, ruta)
    
    def numero_transferencias(self, objeto1='YOU', objeto2='SAN'):
        orb1 = set(self.obtener_ruta_orbita(objeto1))
        orb2 = set(self.obtener_ruta_orbita(objeto2))
        interseccion = orb1.intersection(orb2)
        return (len(orb1-interseccion) + len(orb2-interseccion))

# %%
path = "d:\\advent-of-code-2019\\day6\\"
with open(path+"input.txt") as input:
    datos_mapa = [orb.strip() for orb in input]

mapa = Mapa(datos_mapa)
mapa.extraer_objetos()
print(mapa.cuenta_orbitas_total())
# %%
mapa_prueba = Mapa(['COM)B','B)C','C)D','D)E','E)F','B)G','G)H','D)I','E)J','J)K','K)L','K)YOU','I)SAN'])
print(mapa_prueba.numero_transferencias())
# %%
print(mapa.numero_transferencias())

# %%
