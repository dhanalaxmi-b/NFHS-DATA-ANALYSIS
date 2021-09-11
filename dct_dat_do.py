import numpy as np
import pandas as pd
import re

dat_file = r"E:\CStep\work\NFHS_Data\Children_IAKR74FL\IAKR74FL.dat" 
dct_file = "IAKR74FL.dct"   
do_file = "IAKR74FL.do"



col_names = []
with open(dct_file) as infile:
    for line in infile.read().splitlines()[2:-1]:
        l = []
        l+= [line.split()[1], line.split()[0]]
        l1 = line.split(":")[1].strip().split("-")
        l = l+[int(l1[0])-1,int(l1[1])]
        col_names.append(l)
        
with open(do_file) as dfile:
    col_dict = {}
    for line in dfile.read().splitlines()[2:]:
        if re.search(r'^label variable', line):
            col_dict[line.split()[2]] = re.findall(r'"([^"]*)"', line)[0]
        else:
            continue
        
with open(dat_file) as f:
    df_list = []
    count = 0
    for line in f.read().splitlines():
        #print(line)
        dd = []
        for var in col_names:
            dd.append(line[var[2]:var[3]].strip())
        df_list.append(dd)
        print(count)
        count+=1

col = [i[0] for i in col_names]
df = pd.DataFrame(df_list, columns = col)

with open(do_file) as dfile:
    col_codes = dfile.read().split("#delimit ;")[1].split(";")[:-1]
    
label_define = {}
for col in col_codes:
    inner_line = col.strip().split("\n")
    label_define[inner_line[0].strip().split()[2].lower()]={x[0].strip():x[1] for x in [inner_line[code].strip().split('"')[:-1] for code in range(1, len(inner_line))]}

df1 = df.copy()
df1.replace(label_define,inplace=True)
df1.rename(columns=col_dict, inplace=True)
df1.to_excel('df1.xlsx')
    
    
# filter Karnataka dataset
df = df[df.v024 == '16']
    
df1 = df.copy()
df1.replace(label_define,inplace=True)
df1.rename(columns=col_dict, inplace=True)
df1.to_excel('df1.xlsx')

df.to_excel('df.xlsx')
df1.to_excel('df1.xlsx')