import pandas as pd
fname = '%s.xlsx'
df = pd.read_excel(fname,sheet_name="Sheet1")
mylist = df["pea"].tolist()
pea1 = []
for i in mylist :
    pea1.append(i)
print(pea1)