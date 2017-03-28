import pickle


def importGameElement(fileName):
    return pickle.load( open( fileName, "rb" ) )
    
def exportGameElement(fileName,myMap):
    pickle.dump( myMap, open( fileName, "wb" ) )
    
def importZone(fileName):
    #imports a zone from a zonefile. 
    lineNum=1
    COLLISIONS= []
    with open(fileName) as f:
        for line in f:
            if(lineNum is 1):
                image = line.strip()
            elif(lineNum is 2):
                parsed = line.split(',')
                MAPWIDTH = int(parsed[0])
                MAPHEIGHT = int(parsed[1])
            else:
                COLLISIONS.append([int(x) for x in line.split(',')])
            lineNum+=1
    return image,MAPWIDTH,MAPHEIGHT,COLLISIONS
            
        
        