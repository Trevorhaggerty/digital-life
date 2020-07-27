






import sys
import time
from os import system, name 


grayscalewtb = "$@B%8&WM#oahkbdpqwmZO0QLYXCJUzcvunxrjft/\|()1{}[]?<>i!lI;:+~,.- "
grayscalebtw = ''.join(reversed(grayscalewtb))

def clearScreen():
    if name == 'nt': 
	    _ = system('cls')
    else: 
	    _ = system('clear') 

k = 64
for t in range(-k, k):
    print('i&j&t', end = '')
    for i in range(k):
        if i < 10:
            print(str(i), end = '  ')
        else:
            print(str(i), end = ' ')
    print()
    for i in range(k):
        print('---', end = '')
    print()
    for j in range(k):
        if j < 10:
            print(str(j), end ="  : ")
        else:
            print(str(j), end =" : ")
        for i in range(k):
            print(str(grayscalebtw[i&j&t]) + str(grayscalebtw[i&j&t ]), end =" ")
        print()
    if t > 0:
        time.sleep(.75)
    else :
        time.sleep(.5)
    clearScreen()