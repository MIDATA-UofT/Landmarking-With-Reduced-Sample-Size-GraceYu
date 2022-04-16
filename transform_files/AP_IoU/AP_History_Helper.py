# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:53:17 2022

@author: GraceYu
"""

import json
import xlsxwriter
import math
data = []
for line in open('metrics.json', 'r'):
    data.append(json.loads(line))


list_AP = []
# find out the mAPs
for each in data:
    if "bbox/AP" in each:
        list_AP.append(each)
        
# save it to a new Json file
with open ("AP_History.json", 'w') as new_json:
    json.dump(list_AP, new_json)
new_json.close()

# save it to excel
# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('AP_History.xlsx')
 
# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

row = 0
column = 0
# first create titles
for key in list_AP[0]:
    worksheet.write(row, column, key)
    column+=1

row = 1
for history in list_AP:
    column = 0
    for key, value in history.items():
        if math.isnan(value):
            worksheet.write(row, column, "NA")
        else:
            worksheet.write(row, column, value)
        column+=1
    row += 1
workbook.close()

        