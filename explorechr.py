#explore char values
import sys

rows = 10
x = 0
stringBuffer2 = ''
while x < 55295 / 2:
    if x == 0 :
        stringBuffer1 = "integer = character\n"
    stringBuffer1 = str(x) + ' = ' + chr(x)
    if x % rows == rows - 1 :
        stringBuffer1 = stringBuffer1 + '\n'
    else :
        stringBuffer1 = stringBuffer1 + ' | '
    stringBuffer2 = stringBuffer2 + stringBuffer1
    print(stringBuffer1, end='')
    x += 1
x = 0
chrValues = open( 'charvalues.txt','x')

while x < len(stringBuffer2) :
    try :
        print (stringBuffer2[x], end = '')
        chrValues.write(stringBuffer2[x])
        x += 1
    except UnicodeEncodeError as detail :
        print ('x = ' + str(x) +' does not work'), detail
        x +=1

chrValues.close