import random
from fractions import Fraction
import re

class ProblemGenerator:
    def __init__(self, difficulty=1) -> None:
        self.difficulty = difficulty

    def checkAnswer(self, answer:str, input:str):
        if re.fullmatch(r"[-]?[0-9]*\.?[0-9]*", input):
            return abs(float(answer) - float(input)) < 0.01
        elif re.fullmatch(r"[-]?[1-9][0-9]*\/[-]?[1-9][0-9]*", input):
            frac = input.split('/')
            return (str(Fraction(answer).limit_denominator(100).numerator) == frac[0] and 
                    str(Fraction(answer).limit_denominator(100).denominator) == frac[1])
        else:
            return False

    # PLACEHOLDER FOR NOW. WILL DIVERSITY QUESTION TYPES LATER
    def new_problem(self, category):
        if category in {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}:
            match category:
                case 1 | 2 | 3:
                    return self.addndigit(category)
                case 4 | 5 | 6:
                    return self.subndigit(category-3)
                case 7:
                    return self.mult12()
                case 8:
                    return self.div12()
                case 9:
                    return self.multndigit(2)
                case 10:
                    return self.divnfrac(2)
                
        return self.addndigit(category)


    def mult12(self):
        a = random.randint(2, 12)
        b = random.randint(2, 12)

        return {
            "prompt" : f"{a} x {b} = ",
            "answer" : f"{a * b}",
            "value" : 1.3
        }
    
    def multndigit(self, n):
        a = random.randint(10**(n-1), 10**n - 1)
        b = random.randint(10**(n-1), 10**n - 1)

        return {
            "prompt" : f"{a} x {b} = ",
            "answer" : f"{a * b}",
            "value" : -2 + 3*n
        }
    
    def div12(self):
        a = random.randint(2, 12)
        b = random.randint(2, 12)

        return {
            "prompt" : f"{a*b} / {b} = ",
            "answer" : f"{a}",
            "value" : 1.35
        }
    
    def divnfrac(self, n):
        if n > 1:
            common_div = random.randint(2, 10*n)
            a_div = random.randint(3, (10**n-1)//common_div)
            b_div = random.randint(3, (10**n-1)//common_div)
            while b_div == a_div:
                b_div = random.randint(3, (10**n-1)//common_div)
            a = common_div * a_div
            b = common_div * b_div
        else:
            a = random.randint(2, 12)
            b = random.randint(2, 12)

        return {
            "prompt" : f"Simplify {a} / {b} = ",
            "answer" : f"{a / b}",
            "value" :  -3 + 4*n
        }

       
    def addndigit(self, n):
        a = random.randint(10**(n-1), 10**n - 1)
        b = random.randint(10**(n-1), 10**n - 1)

        return {
            "prompt" : f"{a} + {b} = ",
            "answer" : f"{a + b}",
            "value" : 0.3 * n
        }
    
    def subndigit(self, n):
        a = random.randint(10**(n-1), 10**n - 1)
        b = random.randint(10**(n-1), 10**n - 1)

        return {
            "prompt" : f"{a} - {b} = ",
            "answer" : f"{a - b}",
            "value" : 0.45 * n
        }
    

    




if __name__ == "__main__":
    gen = ProblemGenerator()
    # print(gen.mult12())
    # print(gen.mult12())
    # print(gen.mult12())
    # print(gen.add1())
    # print(gen.add1())
    # print(gen.add1())
    # print(gen.addndigit(3))
    # print(gen.addndigit(3))
    # print(gen.addndigit(5))
    print(gen.checkAnswer(3 , '3')) # true
    print(gen.checkAnswer(245 , '490/2')) #false NOT SIMPLIFIED
    print(gen.checkAnswer(0.5 , '1/2')) # true
    print(gen.checkAnswer(2.5 , '2.5')) # true
    print(gen.checkAnswer(2.5 , '5/2')) # true
    print(gen.checkAnswer(2.5 , '10/4')) # false
    print(gen.checkAnswer(3.333 , '3.33')) # true
    print(gen.checkAnswer(3.333 , '10/3')) # true
    print(gen.checkAnswer(3 , '3'))