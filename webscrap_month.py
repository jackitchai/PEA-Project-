from selenium import webdriver
import bs4
import pandas as pd
import datetime
import ezsheets
find_date = datetime.datetime.now()
if find_date.month < 10 :
    month = "0"+str(find_date.month)
else :
    month = str(find_date.month)
##--- webdriver part
driver = webdriver.Chrome(executable_path=r"C:\Users\511881\Downloads\chromedriver_win32\chromedriver")
last_url = "%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88%2050%20%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B9%80%E0%B8%94%E0%B8%B7%E0%B8%AD%E0%B8%99%20%E0%B8%A0%E0%B8%B2%E0%B8%84%E0%B9%80%E0%B8%AB%E0%B8%99%E0%B8%B7%E0%B8%AD-R1.xml"
driver.get("http://172.30.7.213/reports/report.html?file=reports/R1/50/%s-%s-01-%s"%(find_date.year,month,last_url))
data = driver.page_source
##--- ดึงข้อมูลจาก beautifulsoup เพื่อหาว่ามีกี่หน้าเพจ
bs4_data = bs4.BeautifulSoup(data)
find_page = bs4_data.find_all('span') #หาจำนวนหน้า page
all_data_l = []
##--- ใช้ selenium คลิกเพื่อเปลี่ยนหน้าเพจ
for npage in range (1,len(find_page)-1) :
    number_page = npage+1 
    page_button = driver.find_element("xpath","/html/body/div/span[%s]"%str(number_page)) #หาหน้าเพจ 1,2,3,...เเล้ว click
    page_button.click()
    data = driver.page_source
    ##--- เก็บข้อมูลจาก แต่ละเพจอีกรอบ เพื่อเก็บข้อมูลมาใช้
    bs4_data = bs4.BeautifulSoup(data)
    all_data = bs4_data.find_all('tbody')#หาตารางใช้ beautiful
    tr_data = all_data[1].find_all('tr') #หาเเถว beautiful
    for index in range (len(tr_data)) : #เก็บข้อมูลทุกแถวทุกคอมลัมน์
        data_l = []
        for txt in tr_data[index]:
            if txt.text !="\n" :
                data_l.append(txt.text)
        all_data_l.append(data_l) # location-- duration[6],cause[11],pea[13],casualty[15],load[18]
driver.close()
all_data_t = tuple(all_data_l)
##--- เก็บชื่อจากทุก pea ภาค 1
def getpea(file,sheet) : 
    pea_name = []
    fname = '%s.xlsx'%file #เปิดไฟล์ pea
    df = pd.read_excel(fname,sheet_name=sheet)
    mylist = df["pea"].tolist()
    for i in mylist :
        pea_name.append(i)
    return(pea_name)
list_peaname1,list_peaname2,list_peaname3 = getpea("pea","Sheet1"),getpea("pea","Sheet2"),getpea("pea","Sheet3")
##--- เอาข้อมูลจาก ตารางมาทำเป็น dict
def getdict(sheet) :
    dict_pea = dict.fromkeys(getpea("pea",sheet))
    check_dict = dict.fromkeys(dict_pea,0)
    data = all_data_t
    for i in range(len(data)) :
        if data[i][13] in dict_pea and check_dict[data[i][13]] == 0 :
            dict_pea[data[i][13]] = [float(data[i][6].replace(",","")),[data[i][11]],int(data[i][15].replace(",","")),float(data[i][18].replace(",",""))]
            check_dict[data[i][13]] += 1
        elif data[i][13] in dict_pea and check_dict[data[i][13]] == 1 :
            dict_pea[data[i][13]][0] = dict_pea[data[i][13]][0] + float(data[i][6].replace(",",""))
            dict_pea[data[i][13]][1].append(data[i][11])
            dict_pea[data[i][13]][2] = dict_pea[data[i][13]][2] + int(data[i][15].replace(",",""))
            dict_pea[data[i][13]][3] = dict_pea[data[i][13]][3] + float(data[i][18].replace(",",""))
    return dict_pea
dict_pea1,dict_pea2,dict_pea3 = getdict("Sheet1"),getdict("Sheet2"),getdict("Sheet3")
##--- Clean data จาก dict_pea ให้เหลือสาเหตุเเค่สาเหตุเดียว
def mode_clean(dict) :
    count = 0 
    for peaname in dict.keys() :
        if dict[peaname] is None and count == 0:
            dict[peaname] = [0,"","",""]
            count+=1
        elif dict[peaname] is None and count != 0 :
            dict[peaname] = [count,"","",""]
            count+=1
        else :
            dict[peaname][1] = max(set(dict[peaname][1]),key=dict[peaname][1].count)
    return dict
clean_dict_pea1,clean_dict_pea2,clean_dict_pea3 = mode_clean(dict_pea1),mode_clean(dict_pea2),mode_clean(dict_pea3)
##--- เรียง index ของ minute เอามากสุดไว้บน
def get_minute(dict) :
    a_minute = []
    for minute in dict.values():
        if minute[0] == "" :
            a_minute.append(0)
        else :
            a_minute.append(int(minute[0]))
    return sorted(a_minute),a_minute
minute_sorted_1,all_minute_1 =get_minute(clean_dict_pea1)
minute_sorted_2,all_minute_2 =get_minute(clean_dict_pea2)
minute_sorted_3,all_minute_3 =get_minute(clean_dict_pea3)
minute_sorted_1.sort(reverse=True)
minute_sorted_2.sort(reverse=True)
minute_sorted_3.sort(reverse=True)
##--- แต่ละ pea เพื่อมาจัดเรียงชื่อการไฟฟ้า
def pea_index(pea,minute_sorted,all_minute) :
    index_list = []
    pea_list =[]
    for minute in minute_sorted :
        index_number = all_minute.index(minute)
        index_list.append(index_number)
    for i in index_list :
        pea_list.append(pea[i])
    return pea_list
top_pea1,top_pea2,top_pea3 = pea_index(list_peaname1,minute_sorted_1,all_minute_1)\
    ,pea_index(list_peaname2,minute_sorted_2,all_minute_2),pea_index(list_peaname3,minute_sorted_3,all_minute_3)
##--- ทำข้อมูลจาก dict ให้เป็น list 
def to_excel_list(top_pea,clean_dict_pea) :
    return [clean_dict_pea[i][0] for i in top_pea],[clean_dict_pea[i][1] for i in top_pea]\
        ,[clean_dict_pea[i][2] for i in top_pea],[clean_dict_pea[i][3] for i in top_pea]
dura_1,cause_1,casual_1,load_1 = to_excel_list(top_pea1,clean_dict_pea1)
dura_2,cause_2,casual_2,load_2 = to_excel_list(top_pea2,clean_dict_pea2)
dura_3,cause_3,casual_3,load_3 = to_excel_list(top_pea3,clean_dict_pea3)
##--- ใช้ pandas เรียงข้อมูล
data_excel_s1 = pd.DataFrame([top_pea1,dura_1,cause_1,casual_1,load_1]).transpose()
data_excel_s2 = pd.DataFrame([top_pea2,dura_2,cause_2,casual_2,load_2]).transpose()
data_excel_s3 = pd.DataFrame([top_pea3,dura_3,cause_3,casual_3,load_3]).transpose()
def name_column(data_excel): 
    data_excel.columns = ["การไฟฟ้า","ไฟดับจำนวนนาที","สาเหตุที่เกิดบ่อยที่สุด","จำนวนผู้ได้รับผลกระทบ(รวมทุกสาเหตุ)","รวมโหลดที่เกิดขึ้น(MW)"]
    return data_excel
file_name = "report50_y" + str(find_date.year)+"_m_"+str(find_date.month)
##--- เขียนไฟล์ excel
writer = pd.ExcelWriter("%s.xlsx"%file_name,engine="xlsxwriter")
excel_s1,excel_s2,excel_s3 = name_column(data_excel_s1),name_column(data_excel_s2),name_column(data_excel_s3)
excel_s1.to_excel(writer,sheet_name = "กฟน.1")
excel_s2.to_excel(writer,sheet_name = "กฟน.2")
excel_s3.to_excel(writer,sheet_name = "กฟน.3")
writer.save()
#clientid = 520579458145-d0pc9l6r2e6kogaetcnepacbdeugfjk1.apps.googleusercontent.com
#client secret = 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
##---อัพเข้า google sheet
sheet = ezsheets.Spreadsheet("1aacFR09DE0KF1jGmav7VfsA9Aiav1aIgSqthzaP7jII") #sheet ไฟตกไฟดับ dash board id  = 1aacFR09DE0KF1jGmav7VfsA9Aiav1aIgSqthzaP7jII
sheet_1,sheet_2,sheet_3 = sheet['table 2'],sheet["table 3"],sheet["table 4"]
def update_sheet(sheet,t,d,c) :
    sheet['A2'],sheet['B2'],sheet['C2'] = t[0],d[0],c[0]
    sheet['A3'],sheet['B3'],sheet['C3'] = t[1],d[1],c[1]
    sheet['A4'],sheet['B4'],sheet['C4'] = t[2],d[2],c[2]
    sheet['A5'],sheet['B5'],sheet['C5'] = t[3],d[3],c[3]
    sheet['A6'],sheet['B6'],sheet['C6'] = t[4],d[4],c[4]
    return
update_sheet(sheet_1,top_pea1,dura_1,cause_1)
update_sheet(sheet_2,top_pea2,dura_2,cause_2)
update_sheet(sheet_3,top_pea3,dura_3,cause_3)