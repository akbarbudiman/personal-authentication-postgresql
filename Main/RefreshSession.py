from Support import DefinedException
from datetime import datetime, timedelta

def DoRefreshSession(cursor, sessionID):

    if sessionID is None:
        raise DefinedException.throwException("personal.authentication.refreshSession.invalidSessionID")
    if type(sessionID) != str:
        raise DefinedException.throwException("personal.authentication.refreshSession.invalidSessionID")

    retrieveSessionQuery = """SELECT userid FROM "session" WHERE sessionid='%s' AND isvalid=true AND sessionexpiration>CURRENT_TIMESTAMP;""" % sessionID
    cursor.execute(retrieveSessionQuery)
    retrieveSessionResponse = cursor.fetchall()

    if len(retrieveSessionResponse) != 1:
        raise DefinedException.throwException("personal.authentication.refreshSession.invalidSessionID")

    userID = retrieveSessionResponse[0][0]
    newSessionExpiration = str(datetime.now() + timedelta(hours=4))
    updateSessionQuery = """UPDATE "session" SET sessionexpiration=%s WHERE userid=%s AND sessionid=%s;"""
    updateSessionParameter = (
        newSessionExpiration,
        userID,
        sessionID
    )
    cursor.execute(updateSessionQuery, updateSessionParameter)

    response = {
        "userID": userID
    }
    return response