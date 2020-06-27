from flask import Flask, request, jsonify
from Main import Register, Login, RefreshSession, ChangePassword, Logout
from Support import Connection
from Support.DefinedException import DefinedException

app = Flask(__name__)

Connection.initDatabase()

@app.route("/")
def home():
    return "Hello, Welcome to my Authentication application!"

@app.route("/auth/register", methods=["POST"])
def processRegister():
    (connection, cursor) = Connection.createConnection()
    requestBody = request.get_json()

    try :
        registerResponse = Register.DoRegister(cursor, requestBody)
        connection.commit()
        return jsonify(registerResponse)
    except DefinedException as definedError:
        errorCode = definedError.errorCode
        exceptionResponse = buildExceptionResponse(cursor, errorCode)
        return jsonify(exceptionResponse)
    except:
        raise
    finally:
        Connection.closeConnection(connection, cursor)

@app.route("/auth/login", methods=["POST"])
def processLogin():
    (connection, cursor) = Connection.createConnection()
    requestBody = request.get_json()

    try :
        loginResponse = Login.DoLogin(cursor, requestBody)
        connection.commit()
        return jsonify(loginResponse)
    except DefinedException as definedError:
        errorCode = definedError.errorCode
        exceptionResponse = buildExceptionResponse(cursor, errorCode)
        return jsonify(exceptionResponse)
    except:
        raise
    finally:
        Connection.closeConnection(connection, cursor)

@app.route("/auth/logout", methods=["POST"])
def processLogout():
    (connection, cursor) = Connection.createConnection()
    requestBody = request.get_json()

    try :
        logoutResponse = Logout.DoLogout(cursor, requestBody)
        connection.commit()
        return jsonify(logoutResponse)
    except DefinedException as definedError:
        errorCode = definedError.errorCode
        exceptionResponse = buildExceptionResponse(cursor, errorCode)
        return jsonify(exceptionResponse)
    except:
        raise
    finally:
        Connection.closeConnection(connection, cursor)

@app.route("/auth/change-password", methods=["POST"])
def processChangePassword():
    (connection, cursor) = Connection.createConnection()
    requestBody = request.get_json()

    try :
        refreshSessionResponse = RefreshSession.DoRefreshSession(cursor, requestBody.get("sessionID"))
        requestBody.update(refreshSessionResponse)
        changePasswordResponse = ChangePassword.DoChangePassword(cursor, requestBody)
        connection.commit()
        return jsonify(changePasswordResponse)
    except DefinedException as definedError:
        errorCode = definedError.errorCode
        exceptionResponse = buildExceptionResponse(cursor, errorCode)
        return jsonify(exceptionResponse)
    except:
        raise
    finally:
        Connection.closeConnection(connection, cursor)

@app.route("/auth/refresh-session", methods=["GET"])
def processRefreshSession():
    (connection, cursor) = Connection.createConnection()
    sessionID = request.args.get('sessionid')

    try:
        refreshSessionResponse = RefreshSession.DoRefreshSession(cursor, sessionID)
        connection.commit()
        return jsonify(refreshSessionResponse)
    except DefinedException as definedError:
        errorCode = definedError.errorCode
        exceptionResponse = buildExceptionResponse(cursor, errorCode)
        return jsonify(exceptionResponse)
    except:
        raise
    finally:
        Connection.closeConnection(connection, cursor)


def buildExceptionResponse(cursor, errorCode):
    retrieveQuery = """SELECT errorMessage FROM "exception_mapping" WHERE errorcode='%s';""" % errorCode
    cursor.execute(retrieveQuery)
    retrieveQueryResult = cursor.fetchall()

    isErrorDefined = len(retrieveQueryResult) > 0
    if isErrorDefined:
        errorMessage = retrieveQueryResult[0][0]
    else:
        errorCode = ""
        errorMessage = {}

    exceptionResponse = {
        "errorCode": errorCode,
        "errorMessage": errorMessage
    }
    return exceptionResponse


if __name__ == '__main__':
    app.run(debug=False)
