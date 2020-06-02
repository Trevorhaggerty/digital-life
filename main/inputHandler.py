from terrainGenerator import * 


def requestMovementInput():
    requestFiled = False
    while requestFiled == False :
        print("1  ↖ /\ ↗ 2")
        print("6  ⬅| |➡ 3")
        print("5  ↙ \/ ↘ 4")
        valuedCustomerInput = input("enter to continue. type 0 to end\n")
        try :
            direction = int(valuedCustomerInput) -1
            requestFiled = True
        except EnvironmentError as errorMessage:
            print(errorMessage)
            print('please try again')
    return direction

def moveEntity(entityID, direction, gameSpace):
    if checkNeighbor(gameSpace.entityList[entityID].x, gameSpace.entityList[entityID].y, 0, gameSpace)[direction] == 1:
        if gameSpace.entityList[entityID].y % 2 != 0:
            if direction == 0:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y -= 1
            if direction == 1:
                gameSpace.entityList[entityID].x += 0 
                gameSpace.entityList[entityID].y -= 1
            if direction == 2:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 0
            if direction == 3:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y += 1
            if direction == 4:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 1
            if direction == 5:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 0
        elif gameSpace.entityList[entityID].y % 2 == 0:
            if direction == 0:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y -= 1
            if direction == 1:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y -= 1
            if direction == 2:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 0
            if direction == 3:
                gameSpace.entityList[entityID].x += 1
                gameSpace.entityList[entityID].y += 1
            if direction == 4:
                gameSpace.entityList[entityID].x += 0
                gameSpace.entityList[entityID].y += 1
            if direction == 5:
                gameSpace.entityList[entityID].x -= 1
                gameSpace.entityList[entityID].y += 0
    else:
        print('the way is blocked')
    return False