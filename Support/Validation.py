from Support import DefinedException

def ifNullThrow(objectToCheck, errorMessage):
    if errorMessage == None:
        if objectToCheck == None:
            raise DefinedException.throwException("something should not be null")
    elif isinstance(errorMessage, str):
        if objectToCheck == None:
            raise DefinedException.throwException(errorMessage)
    else:
        pass