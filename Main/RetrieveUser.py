def RetrieveUserByPrincipal(cursor, principal):
    retrieveQuery = """SELECT userid, principal, principaltype, password FROM "user" WHERE principal='%s';""" % principal
    cursor.execute(retrieveQuery)
    retrievedResponse = cursor.fetchall()

    userList = []
    for oneRow in retrievedResponse:
        oneUser = {
            "userid": oneRow[0],
            "principal": oneRow[1],
            "principalType": oneRow[2],
            "password": oneRow[3]
        }
        userList.append(oneUser)

    return userList

def RetrieveUserByUserID(cursor, userID):
    retrieveQuery = """SELECT userid, principal, principaltype, password FROM "user" WHERE userID=%s;""" % userID
    cursor.execute(retrieveQuery)
    retrievedResponse = cursor.fetchall()

    userList = []
    for oneRow in retrievedResponse:
        oneUser = {
            "userid": oneRow[0],
            "principal": oneRow[1],
            "principalType": oneRow[2],
            "password": oneRow[3]
        }
        userList.append(oneUser)

    return userList