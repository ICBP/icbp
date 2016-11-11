# START CODE
# import the mysql module
import pymysql.cursors

# connect to the database you created with the credentials you set up
connection = pymysql.connect(host='localhost',
    user='root',
    password='root',
    db='arduino',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
# END CODE

# START CODE
# set the following variables with the calculated values you want to store
value1 = 110
value2 = 13
value3 = 1232

# This will create a row of data in the database if all goes as planned
with connection.cursor() as cursor:
    sql = "INSERT INTO data (val1, val2, val3) VALUES (%s, %s, %s)"
    cursor.execute(sql,(value1,value2,value3))
    connection.commit()
# END CODE

# START CODE
# close database connection
connection.close()
# END CODE
