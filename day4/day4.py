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
"""

#%%
class Password(object):
    def __init__(self, dig_doble, posicion):
        self.dig_doble = dig_doble
        self.posicion = posicion
        self.passwords = [[self.dig_doble, self.dig_doble]]
    
    def generar_parte_superior(self):
        while(self.posicion <= 3):
            for password in self.passwords:
                for nuevo_digito in enumerate(password[-1], 9):
                    password.append(nuevo_digito)
            self.posicion+=1

        



# %%
