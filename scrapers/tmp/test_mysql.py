import datetime
import mysql.connector

try:
    connection = mysql.connector.connect(option_files='/etc/mysql/scraper.cnf')

    mySql_query = """SELECT * FROM central_tools.auth_user where username = 'scraper'"""


    cursor = connection.cursor()
    cursor.execute(mySql_query)
#    connection.commit()
    print(cursor)
    cursor.close()

except mysql.connector.Error as error:
    print("Failed to connect to database ".format(error))

