from Support import PasswordManagement, Validation, DefinedException
from Main import RetrieveUser
from datetime import datetime, timedelta
import hashlib

def DoLogin(cursor, loginRequestBody):
    validLoginRequest = validateAndCreateLoginRequest(loginRequestBody)

    registeredUser = RetrieveUser.RetrieveUserByPrincipal(cursor, validLoginRequest["principal"])
    if len(registeredUser) == 0:
        raise DefinedException.throwException("personal.authentication.login.unregisteredUser")
    else:
        registeredUser = registeredUser[0]

    isPasswordCorrect = PasswordManagement.CheckPassword(validLoginRequest["password"], registeredUser["password"])
    if isPasswordCorrect == False:
        raise DefinedException.throwException("personal.authentication.login.wrongPassword")

    currentTime = datetime.now()
    userID = registeredUser["userid"]
    sessionID = CreateSessionID(registeredUser["principal"], currentTime)
    sessionExpiration = str(currentTime + timedelta(hours=4))

    updateSessionQuery = """UPDATE "session" SET sessionid=%s, sessionexpiration=%s, isvalid=TRUE WHERE userid=%s;"""
    updateSessionParameter = (
        sessionID,
        sessionExpiration,
        userID
    )
    cursor.execute(updateSessionQuery, updateSessionParameter)

    rowUpdatedCount = cursor.rowcount
    if rowUpdatedCount == 1:
        return LoginResponsePositive(sessionID, sessionExpiration)
    else:
        insertSessionQuery = """INSERT INTO "session"(userid, sessionid, sessionexpiration, isvalid) VALUES(%s, %s, %s, TRUE);"""
        insertSessionParameter = (
            userID,
            sessionID,
            sessionExpiration
        )
        cursor.execute(insertSessionQuery, insertSessionParameter)

        return LoginResponsePositive(sessionID, sessionExpiration)


def validateAndCreateLoginRequest(uncheckedLoginRequest):
    principal = uncheckedLoginRequest.get("principal")
    Validation.ifNullThrow(principal, "personal.authentication.login.invalidPrincipal")
    if isinstance(principal, str) == False:
        raise DefinedException.throwException("personal.authentication.login.invalidPrincipal")

    password = uncheckedLoginRequest.get("password")
    Validation.ifNullThrow(password, "personal.authentication.login.invalidPassword")
    if isinstance(password, str) == False:
        raise DefinedException.throwException("personal.authentication.login.invalidPassword")

    checkedLoginResponse = {
        "principal" : principal,
        "password" : password
    }
    return checkedLoginResponse

def CreateSessionID(principal, currentTime):
    sessionIDIngredients = principal + currentTime.isoformat()
    return hashlib.sha256(sessionIDIngredients.encode()).hexdigest()


def LoginResponsePositive(sessionID, sessionExpiration):
    response = {
        "sessionID": sessionID,
        "sessionExpiration": sessionExpiration
    }
    return response