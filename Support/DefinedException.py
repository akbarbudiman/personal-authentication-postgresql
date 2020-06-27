class DefinedException(Exception):
    def __init__(self, errorCode):
        self.errorCode = errorCode
        super().__init__(self.errorCode)

def throwException(errorCode):
    definedException = DefinedException(errorCode)
    return definedException