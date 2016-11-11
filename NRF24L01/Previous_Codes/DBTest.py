
import time
import math

import pymysql.cursors

##------------------Connect to database-----------------------------##

#connect to the database
connection=pymysql.connect(host='localhost',
                               user='root',
                               password='root',
                               db='arduino',
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)
    
    
##------------------Store to database-----------------------------##
try:
    with connection.cursor() as cursor:
        # Create a new record
#       curso.execute("""INSTER INTO data VALUES (%s, %s, %s)""", (1, 2016-10-20 04:04:04, 100, 10, 1300))##
       
        sql = "INSERT INTO data ('ID', 'time' `val1`, `val2`, 'val3') VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql,('1', '2016-10-20 04:04:04', '110', '10', '1100'))

        # connection is not autocommit by default. So you must commit to save your changes.
        connection.commit()

##            with connection.cursor() as cursor:
##                # Read a single record
##                sql = "SELECT `id`, `watts` FROM `Usage` WHERE `watts`=%s"
##                cursor.execute(sql, ('1200',))
##                result = cursor.fetchone()
##                print(result)

finally:
    connection.close()
