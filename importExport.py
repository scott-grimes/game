import cPickle


def importGameElement(fileName):
    return cPickle.load( open( fileName, "rb" ) )
    
def exportGameElement(fileName,myMap):
    cPickle.dump( myMap, open( fileName, "wb" ) )
    