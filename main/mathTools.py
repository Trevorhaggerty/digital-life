import numpy as np
import uuid

def rndID():
    return uuid.uuid4()
    
def lerp(a , b, t):
    return a + (b - a) * t


#distance and comparison 
def mdDistance(vector1, vector2):
    if len(vector1) != len(vector2):
        return -1
    else:
        b = np.subtract(vector1,vector2)
        b = np.power(b,2)
        s = sum(b)
        distance = np.sqrt(s)
    return distance

def wmdDistance(vector1,vector2,weightVector):
    v1 = np.multiply(vector1,weightVector)
    v2 = np.multiply(vector2,weightVector)
    return mdDistance(v1,v2)


def angleBetweenVectors(vector1,vector2):
    origin = np.zeros(len(vector1))
    v1Mag = mdDistance(vector1, origin)
    v2Mag = mdDistance(vector2, origin)
    a = vector1 * vector2
    b = sum(a)
    c = b / (v1Mag * v2Mag)

    angle = np.arccos(c) * 180/np.pi
    return angle


#Activation Functions --------------------------------------------
    #Sigmoid and its derivative-----------------------------------
def sigmoid(x):
    try :
        return 1 / (1 + np.exp(-x))
    except ArithmeticError as errorcode :
        #logger.logEvent(errorcode)
        return 0 

def Dsigmoid(x) :
    try :
        return x * (1 - x)
    except ArithmeticError as errorcode :
        #logger.logEvent(errorcode)
        return 0
    #reLu and its derivative--------------------------------------
def reLu(x) :
    if x < 0 :
        return 0
    else:
        return x

def DreLu(x) :
    if x < 0 :
        return 0
    else:
        return 1
    #softplus (the derivative of the softplus is the sigmoid)-----
def softplus(x) :
    try :
        return np.log(1 + np.exp(x)) - 1
    except ArithmeticError as errorcode :
        #logger.logEvent(errorcode)
        return 0

def tanh(x) :
    return np.tanh(x)

def Dtanh(x): 
        return 1.0 - tanh(x) ** 2





    