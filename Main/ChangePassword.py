from Support import Validation, DefinedException, PasswordManagement
from Main import RetrieveUser

def DoChangePassword(cursor, changePasswordRequestBody):
    validChangePasswordRequest = validateAndCreateChangePasswordRequest(changePasswordRequestBody)

    userID = validChangePasswordRequest["userID"]
    selectedUser = RetrieveUser.RetrieveUserByUserID(cursor, userID)[0]

    oldPasswordFromRequest = validChangePasswordRequest["oldPassword"]
    oldPasswordFromDB = selectedUser["password"]
    isOldPasswordCorrect = PasswordManagement.CheckPassword(oldPasswordFromRequest, oldPasswordFromDB)
    if isOldPasswordCorrect == False:
        raise DefinedException.throwException("personal.authentication.changePassword.wrongOldPassword")

    updateUserQuery = """UPDATE "user" SET password=%s WHERE userid=%s;"""
    updateUserParameter = (
        validChangePasswordRequest["hashedNewPassword"],
        userID
    )
    cursor.execute(updateUserQuery, updateUserParameter)

    sessionID = validChangePasswordRequest["sessionID"]
    updateSessionQuery = """UPDATE "session" SET isvalid=FALSE WHERE userid=%s AND sessionid=%s;"""
    updateSessionParameter = (
        userID,
        sessionID
    )
    cursor.execute(updateSessionQuery, updateSessionParameter)

    return ChangePasswordResponsePositive()

def validateAndCreateChangePasswordRequest(uncheckedChangePasswordRequest):
    oldPassword = uncheckedChangePasswordRequest.get("oldPassword")
    Validation.ifNullThrow(oldPassword, "personal.authentication.changePassword.invalidOldPassword")
    if isinstance(oldPassword, str) == False:
        raise DefinedException.throwException("personal.authentication.changePassword.invalidOldPassword")

    newPassword = uncheckedChangePasswordRequest.get("newPassword")
    Validation.ifNullThrow(newPassword, "personal.authentication.changePassword.invalidNewPassword")
    if isinstance(newPassword, str) == False:
        raise DefinedException.throwException("personal.authentication.changePassword.invalidNewPassword")

    confirmNewPassword = uncheckedChangePasswordRequest.get("confirmNewPassword")
    Validation.ifNullThrow(confirmNewPassword, "personal.authentication.changePassword.invalidConfirmNewPassword")
    if isinstance(confirmNewPassword, str) == False:
        raise DefinedException.throwException("personal.authentication.changePassword.invalidConfirmNewPassword")

    if newPassword != confirmNewPassword:
        raise DefinedException.throwException("personal.authentication.changePassword.newPasswordInconsistent")

    hashedNewPassword = PasswordManagement.HashPassword(newPassword)

    checkedChangePasswordRequest = {
        "userID": uncheckedChangePasswordRequest["userID"],
        "sessionID": uncheckedChangePasswordRequest["sessionID"],
        "oldPassword": oldPassword,
        "hashedNewPassword": hashedNewPassword
    }
    return checkedChangePasswordRequest

def ChangePasswordResponsePositive():
    response = {}
    response["isSuccess"] = True
    return response