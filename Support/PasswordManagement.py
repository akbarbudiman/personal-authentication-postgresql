import bcrypt

def HashPassword(stringPassword):
    encodedPassword = stringPassword.encode("utf-8")
    hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
    stringHashedPassword = hashedPassword.decode("utf-8")
    return stringHashedPassword

def CheckPassword(passwordFromRequest, passwordFromDb):
    encodedPasswordFromUser = passwordFromRequest.encode()
    encodedPasswordFromDb = passwordFromDb.encode()
    checkPassword = bcrypt.checkpw(encodedPasswordFromUser, encodedPasswordFromDb)
    return checkPassword