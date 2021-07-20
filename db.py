import mysql.connector as connection
import pandas as pd
try:
    mydb = connection.connect(host="localhost", database = 'Student',user="root", passwd="root",use_pure=True)
    query = "Select * from studentdetails;"
    result_dataFrame = pd.read_sql(query,mydb)
    mydb.close() #close the connection
except Exception as e:
    mydb.close()
    print(str(e))