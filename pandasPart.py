import pandas as pd
import ast

list_of_subjects = []
list_of_slots = []

file_name = r"C:\Users\imrit\OneDrive\Desktop\Projects\FFCS Sorter\TestDataSet.xlsx"
df = pd.read_excel(file_name)

for i in range(len(df)):
    list_of_subjects.append(df.iloc[i, 0])
    temp = df.iloc[i,1]
    list_of_slots.append(ast.literal_eval(f'[{temp}]'))


#print(list_of_slots)
# print(list_of_subjects)
