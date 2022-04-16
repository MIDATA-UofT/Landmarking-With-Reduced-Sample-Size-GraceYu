# -*- coding: utf-8 -*-
"""
Created on Thu Apr 14 22:39:26 2022

@author: GraceYu
"""

import os
from shapely.geometry import Polygon
import xlsxwriter
import math

def cast_string_to_float(box):
    box[0] = float(box[0])
    box[1] = float(box[1])
    box[2] = float(box[2])
    box[3] = float(box[3])
    return box


def convert_coordinate(bbox, image):
    # Given COCO coordinate, return polygon coordinates in shapely
    x1 = int(bbox[0]*image[0])
    y1 = int(bbox[1]*image[1])
    w = int(bbox[2]*image[2])
    h = int(bbox[3]*image[3])
    # print ([(x1-0.5*w, y1-0.5*h), (x1-0.5*w, y1+0.5*h), (x1+0.5*h, y1+0.5*h), (x1+0.5*w, y1-0.5*h)])
    return [(x1-0.5*w, y1-0.5*h), (x1-0.5*w, y1+0.5*h), (x1+0.5*h, y1+0.5*h), (x1+0.5*w, y1-0.5*h)]

def calculate_IoU(prediction, ground_truth, image_size):
    print(sum(prediction), sum(ground_truth))
    if (sum(prediction) == 0 and sum(ground_truth) == 0):
        return math.nan
    
    # return the percentage of intersection
    a1 = convert_coordinate(prediction, image_size)
    a2 = convert_coordinate(ground_truth, image_size)
    inference_polygon = Polygon(a1)
    true_polygon = Polygon(a2)
    if inference_polygon.overlaps(true_polygon):
        # print('overlap')
        return (inference_polygon.intersection(true_polygon).area/true_polygon.area)*100
    else:
        return 0


             
true_files = os.listdir("ground_truth/")   # imagine you're one directory above
predict_files = os.listdir("prediction/")
true_coor = [0, 0, 0, 0]
image_size = [0, 0, 0, 0]
category = -1
comparison = []
score = [0, 0, 0]
boxes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]
# example: [[[score0, prediction0, annotation0, image_size, IoU0], [score, prediction, annotation, IoU]],
# [[score0, prediction0, annotation0, IoU0], [score, prediction, annotation, IoU]], image_address]

for image in true_files:
    each = []
    true_coor = [0, 0, 0, 0]
    for i in range(3):
        each.append([0,  [0, 0, 0, 0],  [0, 0, 0, 0],  [0, 0, 0, 0], 0])


    for prediction in predict_files:
        if image == prediction:
            address1 = os.path.join("ground_truth/", image)
            file1 = open(address1,"r")
            while True:
                result = file1.readline()
                if len(result) == 0:
                    break
                
                category, true_coor[0], true_coor[1], true_coor[2],true_coor[3] = result.split();
                category = int(category)
                true_coor = cast_string_to_float(true_coor)
            
                each[category][2] = true_coor.copy()
            file1.close()
            
            
            address2 = os.path.join("prediction/", prediction)
            file2 = open(address2,"r")
            while True:
                result = file2.readline()
                if len(result) == 0:
                    break
                category, true_coor[0], true_coor[1], true_coor[2],true_coor[3], score, image_size[0], image_size[1], image_size[2],image_size[3] = result.split();
                category = int(category)
                true_coor = cast_string_to_float(true_coor)
                image_size = cast_string_to_float(image_size)
                each[category][1] = true_coor.copy()
                each[category][0] = score
                each[category][3] = image_size.copy()
                # print(each[category][1], each[category][2], each[category][3])
                # print()
                # print(each[category][-1])
            file2.close()

    comparison.append(each)
    
        
    # calculate IoU
    for each in comparison:
        for category in range(3):
                each[category][4]=(calculate_IoU(each[category][1], each[category][2], each[category][3]))
               
    
    workbook = xlsxwriter.Workbook('score.xlsx')
    workbook2 = xlsxwriter.Workbook('IoU.xlsx')
     
    # The workbook object is then used to add new
    # worksheet via the add_worksheet() method.

    worksheet1 = workbook.add_worksheet()
    worksheet1.write(0, 0, 'Femur')
    worksheet1.write(0, 1, 'Patella')
    worksheet1.write(0, 2, 'QT')

    worksheet2 = workbook2.add_worksheet()
    worksheet2.write(0, 0, 'Femur')
    worksheet2.write(0, 1, 'Patella')
    worksheet2.write(0, 2, 'QT')

    row = 1

    for image in comparison:
        for i in range(3):
            worksheet1.write(row, i, image[i][0])

            if math.isnan(image[i][-1]):
                worksheet2.write(row, i, "NaN")
            else:
                worksheet2.write(row, i, image[i][-1])



        row += 1

 
workbook.close()
workbook2.close()
