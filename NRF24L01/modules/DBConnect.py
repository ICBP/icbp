import mysql.connector

config = {
    
    host='localhost',
    user='root',
    password='root',
    db='ICBP',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
}

cnx = mysql.connector.connect(**config)

cnx.close()
