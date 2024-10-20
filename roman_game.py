'''
The idea with this file is that 
1) I have no idea how to actually measure the complexity of an operation
2) So, the way I should figure this out is by coming up with as many features of the incomming numbers
   and then try to match those features to the number of seconds it takes me to actually perform the move
   using a VERY basic ml thing
'''
import random
import time
import threading
from cost import Cost
from roman import RomanNumeral
import ctypes
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

def out(prompt, time, game):
   f = open(f"./logs/{game}.txt", "a")
   f.write(f"{prompt}:{time}\n")

def timerThread():
   stepsize = 0.1 #seconds
   timerThread.working = False
   timerThread.start = time.time_ns()
   timerThread.guesses = 0
   def run():
      while True:
         if timerThread.working:
            print('\033[s', end='\r')
            print(f'\033[{timerThread.guesses + 2}A', end='\r')
            
            print(f"elapsed time: {(time.time_ns() - timerThread.start) / 1000. / 1000. / 1000. :.1f}", end='\r')
            print('\033[u', end='')
            time.sleep(stepsize)
   threading.Thread(target=run, daemon=True).start()
timerThread()

def game(ans, prompt, game):  
   print('\n')
   print(prompt)
   start = time.time_ns()
   timerThread.working = True
   timerThread.start = start
   x = ""
   timerThread.guesses = 0
   while x.lower() != ans.lower():
      x = input()
      timerThread.guesses += 1
      if timerThread.guesses > 6:
         print(ans)
         break
   end = time.time_ns()
   # print("\n" * (timerThread.guesses - 1), end='')
   timerThread.working = False
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

def playDivision(prompts=True):
   r1 = RomanNumeral(random.randint(100, 4000))
   r2 = RomanNumeral(random.randint(1, 100))
   print(f"{r1.pretty()} / {r2.pretty()} = ?")
   cost = Cost()

   phase = 0
   input()
   outstr, _, _ = r1.division_algorithm(r2, cost)
   prev = None
   for operation, left, right, ans in cost.steps[1:]:
      if ans == prev: continue
      if (operation) == "begin phase":
         phase += 1
      else:
         if phase == 0 and operation == "less":
            if ans == "right": continue
            else: ans = "sub"

         if phase == 1 and operation == "less":
            ans = "l" if ans == "right" else "nl"
         

         prompt = f"{left} {operation} {right}" if prompts else ""

         dur = game(ans, prompt, operation)
         out(prompt, dur, operation) 
      prev = ans
   print(outstr)
      
   
# playSumSimplify()
for _ in range(40):
   playDivision(False)