from Support import PasswordManagement, Validation, DefinedException
from Main import RetrieveUser

def DoRegister(cursor, registerRequestBody):
    validRegisterRequest = validateAndCreateRegisterRequest(registerRequestBody)

    registeredUser = RetrieveUser.RetrieveUserByPrincipal(cursor, validRegisterRequest["principal"])
    if len(registeredUser) > 0:
        raise DefinedException.throwException("personal.authentication.register.duplicateUser")

    insertUserQuery = """INSERT INTO "user"(principal, principalType, password) VALUES(%s, %s, %s);"""
    insertUserParameter = (
        validRegisterRequest["principal"],
        validRegisterRequest["principalType"],
        validRegisterRequest["hashedPassword"]
    )
    cursor.execute(insertUserQuery, insertUserParameter)

    return RegisterResponsePositive()

def validateAndCreateRegisterRequest(uncheckedRegisterRequest):
    principal = uncheckedRegisterRequest.get("principal")
    Validation.ifNullThrow(principal, "personal.authentication.register.invalidPrincipal")
    if isinstance(principal, str) == False:
        raise DefinedException.throwException("personal.authentication.register.invalidPrincipal")

    principalType = uncheckedRegisterRequest.get("principalType")
    Validation.ifNullThrow(principalType, "personal.authentication.register.invalidPrincipalType")
    availablePrincipalType = ["email", "phone"]
    if principalType not in availablePrincipalType:
        raise DefinedException.throwException("personal.authentication.register.invalidPrincipalType")

    password = uncheckedRegisterRequest.get("password")
    Validation.ifNullThrow(password, "personal.authentication.register.invalidPassword")
    if isinstance(password, str) == False:
        raise DefinedException.throwException("personal.authentication.register.invalidPassword")
    hashedPassword = PasswordManagement.HashPassword(password)

    checkedRegisterRequest = {
        "principal" : principal,
        "principalType" : principalType,
        "hashedPassword" : hashedPassword
    }
    return checkedRegisterRequest

def RegisterResponsePositive():
    response = {}
    response["isSuccess"] = True
    return response