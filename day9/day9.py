

from intcode import IntCode

if __name__ == "__main__":
    # ----- ----- ----- ----- ----- PARTE 1 ----- ----- ----- ----- ----- #
    print("================= PARTE 1 =================")
    intcode = IntCode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99], saltar=False)
    intcode.ejecutar_programa()
    print(f"Prueba 1 ==> {intcode.salidas}")

    intcode = IntCode([1102,34915192,34915192,7,4,7,99,0], saltar=False)
    intcode.ejecutar_programa()
    print(f"Prueba 2 ==> {intcode.salidas}")

    intcode = IntCode([104,1125899906842624,99], saltar=False)
    intcode.ejecutar_programa()
    print(f"Prueba 3 ==> {intcode.salidas}")    
    path = "d:\\advent-of-code-2019\\day9\\"
    with open(path+"input.txt") as input:
        programa = [int(i) for i in input.read().split(',')]
    
    intcode = IntCode(programa.copy(), entradas=[1], saltar=False)
    intcode.ejecutar_programa()
    print(f"Respuesta parte 1 ==> {intcode.salidas}")
    print("================= PARTE 2 =================")
    intcode = IntCode(programa.copy(), entradas=[2], saltar=False)
    try:
        intcode.ejecutar_programa(recursivo=False)
    except:
        print(intcode.iter)
    print(f"Respuesta parte 2 ==> {intcode.salidas}")
    print(f"Número de iteraciones ==> {intcode.iter}")

