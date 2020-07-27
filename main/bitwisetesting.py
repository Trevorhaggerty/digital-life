






import sys

k = 50
for t in range(k):
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
            if i&j&t < 10:
                print(str(i&j&t), end ="  ")
            else:
                print(str(i&j&t), end =" ")
        print()
        sleep()