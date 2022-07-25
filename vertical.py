open_file = open("update.txt","r")
file_r = open_file.read()
s_txt = file_r.split(",")[:-1]
write_file = open("write.txt","a")
for i in s_txt :
    write_file.write(i+"\n")