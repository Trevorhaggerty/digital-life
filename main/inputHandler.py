
def requestContinue():
    requestFiled = False
    while requestFiled == False :
        valuedCustomerInput = input("enter to continue. type x to end\n")
        try :
            requestFiled = True
        except EnvironmentError as errorMessage:
            print(errorMessage)
            print('please try again')
    return valuedCustomerInput

def requestMovementInput():
    requestFiled = False
    while requestFiled == False :
        print("1               2")
        print("     ↖ / \ ↗   ")
        print("      /   \ ")
        print("6  ⬅ |     |➡  3")
        print("      \   / ")
        print("     ↙ \ / ↘    ")
        print("5               4")
        valuedCustomerInput = input("enter to continue. type 0 to end\n")
        try :
            direction = int(valuedCustomerInput) -1
            requestFiled = True
        except EnvironmentError as errorMessage:
            print(errorMessage)
            print('please try again')
    return direction

