import urllib.request
import json 
import mysql.connector
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "user_test"
)
mycursor = mydb.cursor()
user_number = 498949
url = "http://mba.pea.co.th/index.php?emp=%s"
base_url = url%(user_number)
open_url = urllib.request.urlopen(base_url)
json_data = json.loads(open_url.read())
list = json_data["data"]["dataDetail"]
for i in range(len(list)) :
    emp_id = list[i].get("emp_id")
    user_ID = emp_id
    sql = "SELECT * FROM user WHERE userPea =%s"
    val = [(user_ID)]
    m_execute = mycursor.execute(sql,val)
    myresult = mycursor.fetchall()
    for x in myresult :
        print(x)
sql = "SELECT userPea FROM user"
m_execute = mycursor.execute(sql)
myresult = mycursor.fetchall()
for x in myresult :
    print(x)