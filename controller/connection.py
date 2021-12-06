from mysql.connector import connect

def connectToDatabase():
    try:
        mydb = connect(
          host="lochnagar.abertay.ac.uk",
          user="sql1900598",
          password="NuY8Dd2ab85D",
          database="sql1900598"
        )
        return mydb.cursor(prepared=True), mydb
    except:
        print('not connected to the firewall')





    
