"""
--- Day 4: Secure Container ---
You arrive at the Venus fuel depot only to discover it's protected by a password. The Elves had written the password on a sticky note, but someone threw it out.

However, they do remember a few key facts about the password:

It is a six-digit number.
The value is within the range given in your puzzle input.
Two adjacent digits are the same (like 22 in 122345).
Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
Other than the range rule, the following are true:

111111 meets these criteria (double 11, never decreases).
223450 does not meet these criteria (decreasing pair of digits 50).
123789 does not meet these criteria (no double).
How many different passwords within the range given in your puzzle input meet these criteria?

Your puzzle input is 158126-624574.

--- Part Two ---
An Elf just remembered one more important detail: the two adjacent matching digits are not part of a larger group of matching digits.

Given this additional criterion, but still ignoring the range rule, the following are now true:

112233 meets these criteria because the digits never decrease and all repeated digits are exactly two digits long.
123444 no longer meets the criteria (the repeated 44 is part of a larger group of 444).
111122 meets the criteria (even though 1 is repeated more than twice, it still contains a double 22).
How many different passwords within the range given in your puzzle input meet all of the criteria?

"""
class Passwords(object):
    def __init__(self, lim_inf, lim_sup):
        self.lim_inf = lim_inf
        self.lim_sup = lim_sup
    
    def es_creciente(self):
        for i in range(len(self.p_lista_)-1):
            if self.p_lista_[i] > self.p_lista_[i+1]:
                return False
        return True
    
    def tiene_duplicados(self):
        for i in range(len(self.p_lista_)-1):
            if self.p_lista_[i] == self.p_lista_[i+1]:
                return True
        return False
       
    def generar(self):
        self.passwords_ = []
        for p in range(self.lim_inf, self.lim_sup + 1):
            self.p_lista_ = [int(d) for d in str(p)]
            if self.es_creciente() and self.tiene_duplicados():
                print(f"Password encontrada: {self.p_lista_}")
                self.passwords_.append(self.p_lista_)
    
    def filtrar_grupos(self):
        self.passwords_long2_ = []
        for p in self.passwords_:            
            for d in set(p):
                i = p.index(d)
                if (i + 1) < len(p) and p[i] == p[i+1]:
                    if (i + 2 == len(p)) or p[i+2] != p[i+1]:
                        print(f"Password con un grupo de dos dígitos repetidos exactamente encontrado: {p}")
                        self.passwords_long2_.append(p)
                        break                  

if __name__ == '__main__':
    passwords = Passwords(158126, 624574)
    passwords.generar()
    print("=======================================")
    print(f"Número total de passwords encontradas: {len(passwords.passwords_)}" )

    print("============== PARTE 2 ================")
    passwords.filtrar_grupos()
    print("=========================================================================================")
    print(f"Número total de passwords encontradas: {len(passwords.passwords_long2_)}" )
