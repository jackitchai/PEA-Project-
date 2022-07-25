from selenium import webdriver
import bs4
import pandas as pd
driver = webdriver.Chrome(executable_path=r"C:\Users\511881\Downloads\chromedriver_win32\chromedriver")
driver.get("http://172.30.7.213/reports/report.html?file=reports/R1/50/2022-07-01-%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B8%87%E0%B8%B2%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88%2050%20%E0%B8%A3%E0%B8%B2%E0%B8%A2%E0%B9%80%E0%B8%94%E0%B8%B7%E0%B8%AD%E0%B8%99%20%E0%B8%A0%E0%B8%B2%E0%B8%84%E0%B9%80%E0%B8%AB%E0%B8%99%E0%B8%B7%E0%B8%AD-R1.xml")
data = driver.page_source
bs4_data = bs4.BeautifulSoup(data)
all_data = bs4_data.find_all('tbody')
tr_data = all_data[1].find_all('tr')
all_data_l = []
for index in range (len(tr_data)) :
    data_l = []
    for txt in tr_data[index]:
        if txt.text !="\n" :
            data_l.append(txt.text)
    all_data_l.append(data_l)
all_data_t = tuple(all_data_l)
print(all_data_t[0][13])
def getpea(file,sheet) :
    pea_name = []
    fname = '%s.xlsx'%file
    df = pd.read_excel(fname,sheet_name=sheet)
    mylist = df["pea"].tolist()
    for i in mylist :
        pea_name.append(i)
    return(pea_name)
