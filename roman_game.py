'''
The idea with this file is that 
1) I have no idea how to actually measure the complexity of an operation
2) So, the way I should figure this out is by coming up with as many features of the incomming numbers
   and then try to match those features to the number of seconds it takes me to actually perform the move
   using a VERY basic ml thing
'''
import random
import time
from cost import Cost
from roman import RomanNumeral

def out(prompt, time, game):
   f = open(f"./logs/{game}.txt", "a")
   f.write(f"{prompt}:{time}")

def game(ans, prompt, game):
   print(prompt)
   start = time.time_ns()
   x = ""
   guesses = 0
   while x != ans:
      x = input()
      guesses += 1
      if guesses > 4:
         print(ans)
         break
   end = time.time_ns()
   out(prompt, end, game)
   return end-start


def playSimplify():
   vals = [random.randint(0, grouping * 2) for grouping in RomanNumeral.group_letters]
   r = ''.join([l * v for l, v in zip(vals, RomanNumeral.place_letters)])

   ans_numeral = RomanNumeral.from_str(r)
   ans_numeral.simplify(Cost())
   ans = ans_numeral.pretty()
   
   dur = game(ans, r, "simplify")

   print(f"it took you {dur / 1000. / 1000. / 1000.} to get the correct answer")

def playSumSimplify():
   r1 = RomanNumeral(random.randint(1, 4000))
   r2 = RomanNumeral(random.randint(1, 4000))

   r3 = r1.sum(r2, Cost())

   r3.simplify(Cost())

   ans = r3.pretty()
   dur = game(ans, f"{r1.pretty()} + {r2.pretty()}", "sumsimplify")

   print(f"it took you {dur / 1000. / 1000. / 1000.}s to get the right answer")

def playDivision():
   r1 = RomanNumeral(random.randint(100, 4000))
   r2 = RomanNumeral(random.randint(1, 100))
   print(f"{r1.pretty()} / {r2.pretty()} = ?")
   cost = Cost()

   r1.division_algorithm(r2, cost)
   input()
   for operation, left, right, ans in cost.ops:
      game(ans, f"{operation} {left} {right}", operation)
   
# playSumSimplify()
for _ in range(40):
   playDivision()