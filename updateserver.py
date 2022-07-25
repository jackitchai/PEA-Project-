import urllib.request
import json 
import mysql.connector
import time
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = "user_test"
)
mycursor = mydb.cursor()
open_file = open("check.txt","r")
file_r = open_file.read()
last_number = file_r.split(",")[-2]
last_number_t = [last_number]
print(last_number_t)
count = len(file_r.split(","))-2
sql = "SELECT userPea FROM user WHERE userPea>%s"
m_execute = mycursor.execute(sql,last_number_t)
myresult = mycursor.fetchall()
open_file.close()
for x in myresult :
  count+=1
  print(str(x)+" ,count number :%d"%count)
  user_number = x[0]
  url = "http://mba.pea.co.th/index.php?emp=%s"
  base_url = url%(user_number)
  open_url = urllib.request.urlopen(base_url)
  json_data = json.loads(open_url.read())
  list = json_data["data"]["dataDetail"]
  for i in range(len(list)) :
    get_data = list[i].get("emp_id")
    pea_code  = list[i].get("pea_code") 
    stell_text_full = list[i].get("stell_text_full")
    dept_sap_full = list[i].get("dept_sap_full")
    business_area_name = list[i].get("business_area_name")
    posi_text = list[i].get("posi_text")
    dept_short = list[i].get("dept_short")
    dept_full = list[i].get("dept_full")
    update_data = "UPDATE user SET pea_code = %s,stell_text_full =%s,dept_sap_full=%s,business_area_name =%s,posi_text=%s,dept_short=%s,dept_full=%s WHERE userPea = %s "
    val = (pea_code,stell_text_full,dept_sap_full,business_area_name,posi_text,dept_short,dept_full,get_data)
    update_exe = mycursor.execute(update_data,val)
    mydb.commit()
    print(mycursor.rowcount,"record(s) affected")
    if mycursor.rowcount == 1 :
      update_number = open("update.txt","a")
      update_number.write(str(get_data)+",")
    file_a = open("check.txt","a") 
    file_a.write(str(get_data)+",")
    time.sleep(3)
file_a.close()
update_number()
    # select_user = "SELECT * FROM user WHERE userPea =%s"
    # val = [(get_data)]
    # m_execute_val = mycursor.execute(select_user,val)
    # myresult_val = mycursor.fetchall()
    # for j in myresult_val :
    #   print(j)