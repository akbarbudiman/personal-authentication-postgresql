from Support import Validation, DefinedException

def DoLogout(cursor, logoutRequestBody):
    validLogoutRequest = validateAndCreateLogoutRequest(logoutRequestBody)

    sessionID = validLogoutRequest["sessionID"]
    updateSessionQuery = """UPDATE "session" SET isvalid=FALSE WHERE sessionid=%s;"""
    updateSessionParameter = (
        sessionID,
    )
    cursor.execute(updateSessionQuery, updateSessionParameter)
    rowUpdatedCount = cursor.rowcount

    if rowUpdatedCount == 1:
        return LogoutResponsePositive()
    else:
        raise DefinedException.throwException("personal.authentication.logout.invalidSessionID")

def validateAndCreateLogoutRequest(uncheckedLogoutRequest):
    sessionID = uncheckedLogoutRequest.get("sessionID")
    Validation.ifNullThrow(sessionID, "personal.authentication.logout.invalidSessionID")
    if isinstance(sessionID, str) == False:
        raise DefinedException.throwException("personal.authentication.logout.invalidSessionID")

    checkedLogoutRequest = {
        "sessionID": sessionID
    }
    return checkedLogoutRequest

def LogoutResponsePositive():
    response = {
        "isSuccess": True
    }
    return response
