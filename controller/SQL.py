from connection import connectToDatabase

def userVerify(p1, p2):
    conn, mydb = connectToDatabase()
    sqlString = "SELECT username FROM cmp307logins WHERE username = %s AND password = %s"
    conn.execute(sqlString, (p1,p2))
    return conn.fetchall()


