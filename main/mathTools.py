#libraries
import numpy as np
import uuid

# ----------------------------------------------------------------------------------------
#rndID creates a unique ID to tag entities and special objects
#   it returns:
#       - a uuid4
def rndID():
    return uuid.uuid4()

# ----------------------------------------------------------------------------------------
#lerp - linear interpolation - evaluates two values, a and b, and some number between 0,1 to give a
#   value that falls inbetween the a and b   
#   it takes in:
#       - a (the first value)
#       - b (the second value)
#       - k (the proportion to return)
#   and it returns:
#       - the value at k proportion between a and b
def lerp(a, b, k):
    return a + (b - a) * k


# ----------------------------------------------------------------------------------------
#vDistance evaluates the distance between 2 vectors of the same shape in euclidian space
#   it takes in:
#       - 2 location vectors
#   and it returns:
#       - the distance between them
def vDistance(vector1, vector2):
    #if the shapes of the vectors are not the same
    if len(vector1) != len(vector2):
        #return an error
        return -1
    #if the chapes of the vectors match
    else:
        #subtracts the vectors along the same dimensions
        b = np.subtract(vector1, vector2)
        #square the result
        b = np.power(b, 2)
        #add each element of the resulting vector
        s = sum(b)
        #square root the result to get the distance
        distance = np.sqrt(s)
    #when completed return the 
    return distance

# ----------------------------------------------------------------------------------------
#wvDistance evaluates the distance between two vectors with specific dimensions magnitude
#   effected by a third 'weight' vector
#   it takes in:
#       - 2 location vectors
#       - a weight vector
#   and it returns:
#       - the weighted distance between them
def wvDistance(vector1, vector2, weightVector):
    v1 = np.multiply(vector1, weightVector)
    v2 = np.multiply(vector2, weightVector)
    return vDistance(v1, v2)

# ----------------------------------------------------------------------------------------
#angleBetweenVectors takes in 2 vectors and returns the angle between them where the 
#   corner between them is the origin
#   it takes in:
#       - 2 vectors of same size
#   and it returns:
#       - angle 
def angleBetweenVectors(vector1, vector2):
    #create an origin vector for analysis reasons
    origin = np.zeros(len(vector1))
    #save the magnitude of the first vector
    v1Mag = vDistance(vector1, origin)
    #save the magnitude of the second vector
    v2Mag = vDistance(vector2, origin)
    #multiply the vectors
    a = vector1 * vector2
    #get the sum of the result of multiplication
    b = sum(a)
    #divide the sum by the combined magnitude to get a third line for angle finding
    c = b / (v1Mag * v2Mag)
    #convert angle from rads to degrees
    angle = np.arccos(c) * 180/np.pi

    return angle


# Activation Functions --------------------------------------------
#NEEDS COMMENTING!!!!!!!!
# ----------------------------------------------------------------------------------------
# sigmoid squishing function
#   it takes in:
#       - a value
#   and it returns:
#       - a value between 1 and 0
def sigmoid(x):
    try:
        return 1 / (1 + np.exp(-x))
    except ArithmeticError as errorcode:
        # logger.logEvent(errorcode)
        return 0

def Dsigmoid(x):
    try:
        return x * (1 - x)
    except ArithmeticError as errorcode:
        # logger.logEvent(errorcode)
        return 0
    # reLu and its derivative--------------------------------------


def reLu(x):
    if x < 0:
        return 0
    else:
        return x
def DreLu(x):
    if x < 0:
        return 0
    else:
        return 1

    # softplus (the derivative of the softplus is the sigmoid)-----
def softplus(x):
    try:
        return np.log(1 + np.exp(x)) - 1
    except ArithmeticError as errorcode:
        # logger.logEvent(errorcode)
        return 0


def tanh(x):
    return np.tanh(x)
def Dtanh(x):
    return 1.0 - tanh(x) ** 2
