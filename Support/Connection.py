import psycopg2
from Support import Constant

def createConnection():
    constant = Constant
    try:
        connection = psycopg2.connect(
            user = constant.DATABASE_USERNAME,
            password = constant.DATABASE_PASSWORD,
            host = constant.DATABASE_HOST,
            port = constant.DATABASE_PORT,
            database = constant.DATABASE_DATABASENAME
        )
        cursor = connection.cursor()
        return (connection, cursor)

    except (Exception, psycopg2.Error) as error:
        print("Error while connecting to PostgreSQL", error)

    # finally:
    #     print("WARNING! connection has NOT been closed!")

def closeConnection(connection, cursor):
    if (connection):
        cursor.close()
        connection.close()

def initDatabase():
    (connection, cursor) = createConnection()
    try:
        cursor.execute(open(Constant.DATABASE_DDL_LOCATION, "r").read())
        connection.commit()
    except Exception as exectionError:
        raise Exception(exectionError)
    finally:
        closeConnection(connection, cursor)

# def insert(tableName, parameter):
#     countParameter = parameter.keys()
#     columnsNameToInsert = parameter.keys()[0]
#     for i in range(1, countParameter):
#         columnsNameToInsert = columnsNameToInsert + parameter.keys()[i]
#


def selectSequenceQuery(sequenceName):
    sequenceQuery = 'SELECT NEXTVAL(%s);' % sequenceName
    return sequenceQuery