from connection import connectToDatabase
from hashlib import md5      

class User:

    accessLevel = ""
    username = ""
    
    def verify(self, username, password): #verify the user
        
        conn, mydb = connectToDatabase()
        sqlString = "SELECT username, accessAll FROM cmp307logins WHERE username = %s AND password = %s"
        password = md5(password.encode()).hexdigest()
        conn.execute(sqlString, (username, password))
        
        data = conn.fetchall()

        if (data):
            self.username = data[0]
            self.accessLevel = data[0][1]

    def logout(self):

        self.accessLevel = ""
        self.username = ""

