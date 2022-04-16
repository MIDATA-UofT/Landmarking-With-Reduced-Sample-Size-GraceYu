# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:50:40 2022

@author: GraceYu
This program take the predicted json file (coco_instances_results.json)
from using unbiased teacher, and generated another json file suitable for 
displaying the images and predictions called predictions_on_test_dataset.json.

The json file _image.coco.json is the json file that contains the testing
dataset, and it is to get the image name and IDs.
information. 
"""

import json, os

cwd = os.getcwd()
outputdir = ("./outputs/10%/inference_14999/")
# get the image information with their ID first because the generated prediction file does not have image info
with open('_image.coco.json', 'r') as json_image_file:
    json_image_load = json.load(json_image_file)
images = json_image_load['images']
info = json_image_load['info']
categories = json_image_load['categories']
json_image_file.close()


# get the predictions/annotations from the prediction file
inputfile = outputdir+'coco_instances_results.json'
with open(inputfile,'r') as json_file:
    json_load = json.load(json_file)

annotations = json_load
# for x in annotations:
#    x['category_id']-=1


# finally give the categories
# Here I manually set the categories
# categories = json_load['categories'], this can only be used if the file contains correct category info
# categories = [{'id':0, 'name':'Femur'}, {'id':1, 'name': 'Patella'}, {'id': 2, 'name': 'Quadriceps Tendon'}]

json_file.close()

new_dict = {'info': info, 'categories': categories, 'images': images, 'predictions':annotations}
outputfile = outputdir+"predictions_on_test_dataset.json"
with open (outputfile, 'w') as new_json:
    json.dump(new_dict, new_json)
new_json.close()