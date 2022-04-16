# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 08:04:57 2022

@author: GraceYu

This file takes the inference data in json format, and select predictions that
meet the threshold confidence. The scores and the boxes of the selected predicitons
are outputted in a json format and in excel.

# The default confidence score threshold is 0.1, and non-max suppression is used.

# IoU is calculated by the intersection area of predicted boxes and annotated boxes.
# If both boxes do not exist, Nan is used for indication. 
"""
# import some common libraries
import numpy as np
import os, json, random
from shapely.geometry import Polygon
import xlsxwriter
import math
import csv



def convert_coordinate(bbox):
    # Given COCO coordinate, return polygon coordinates in shapely
    x1 = bbox[0]
    y1 = bbox[1]
    x2 = (bbox[0]+bbox[2])
    y2 = (bbox[1]+bbox[3])
    return [(x1, y1), (x1, y2), (x2, y2), (x2, y1)]

def calculate_IoU(prediction, ground_truth):
    
    if (sum(prediction) == 0 and sum(ground_truth) == 0):
        return math.nan
    
    # return the percentage of intersection
    a1 = convert_coordinate(prediction)
    a2 = convert_coordinate(ground_truth)
    inference_polygon = Polygon(a1)
    true_polygon = Polygon(a2)
    if inference_polygon.overlaps(true_polygon):
        return (inference_polygon.intersection(true_polygon).area/true_polygon.area)*100
    else:
        return 0


directory = "./"

prediction_file = os.path.join(directory, "predictions_on_test_dataset.json")
truth =  os.path.join(directory, "_annotations.coco.json")
with open(prediction_file, 'r') as json_file:
  json_load = json.load(json_file)
  
with open(truth, 'r') as truth_file:
  truth_load = json.load(truth_file)

images = json_load['images']
predictions = json_load['predictions']
true_annotations = truth_load['annotations']

categories = json_load['categories']
# a dictionary mapping the category ID to the actual structure
classIDs = {}

# record category and associated IDs
for each in categories:
  id = (int) (each['id'])
  category = each['name']
  classIDs[id] = category


total=len(predictions)
# print(total)

# set up the confidence threshold
threshold = 0.1
comparison = [] 
# this is a 3D array/list, for each image (image_id), it stores a 2D array/list
# example: [[[score0, prediction0, annotation0, IoU0], [score, prediction, annotation, IoU]],
# [[score0, prediction0, annotation0, IoU0], [score, prediction, annotation, IoU]], image_address]

    

index = 0
for image_id, image in enumerate(images):
    image_address = image['file_name']
    prediction = predictions[index]
    score = [0, 0, 0]
    boxes = [[0,0,0,0],[0,0,0,0],[0,0,0,0]]

    while(prediction['image_id']==image_id and (index<total)):
        prediction = predictions[index]
        # print('predictions No '+str(index)+'on image '+str(image_id))
        category_id = (int) (prediction['category_id'])
        # round it to two decimal places
        cat_score = round(prediction['score'], 2)
      
        if (score[category_id]<cat_score and cat_score>threshold):
          score[category_id] = cat_score
          boxes[category_id] = prediction['bbox']
      
        index+=1
  
    infer_image = []
    for i in range(3):
        infer_image.append([image_address, score[i], boxes[i], [0, 0, 0, 0]])  
    comparison.append(infer_image)


json_file.close()

# get the true labels
for annotation in true_annotations:
    image_id = annotation['image_id']
    category_id = annotation['category_id']
    comparison[image_id][category_id][3] = annotation['bbox']
    print(comparison[image_id][category_id][2], comparison[image_id][category_id][3])
    print()

truth_file.close()
            
    


for image in comparison:
    for category in image:
        percentage = calculate_IoU(category[2], category[3])
        print(percentage)
        category.append(percentage)
    

# save it to excel
# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.

workbook = xlsxwriter.Workbook('comparison.xlsx')
 
# The workbook object is then used to add new
# worksheet via the add_worksheet() method.

worksheets = [workbook.add_worksheet(), workbook.add_worksheet(), workbook.add_worksheet()]

row = 1

for image in comparison:
    for i in range(3):
        worksheets[i].write(row, 0, row - 1)
        worksheets[i].write(row, 1, image[i][0])
        worksheets[i].write(row, 2, image[i][1])
        
        if math.isnan(image[i][-1]):
            worksheets[i].write(row, 3, "NA")
        else:
            worksheets[i].write(row, 3, image[i][-1])
        for j in range(4):
            worksheets[i].write(row, 4+j, image[i][2][j])
            worksheets[i].write(row, 8+j, image[i][3][j])

    row += 1

workbook.close()

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
            worksheet2.write(row, i, "NA")
        else:
            worksheet2.write(row, i, image[i][-1])


    row += 1

workbook.close()
workbook2.close()




