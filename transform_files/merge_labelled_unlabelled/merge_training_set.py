# -*- coding: utf-8 -*-
"""
Created on Wed Feb 16 17:50:40 2022

@author: GraceYu
"""

import json
# get the image information only from the unlabelled dataset
with open('unlabelled.coco.json', 'r') as json_unlabelled_file:
    json_unlabelled_load = json.load(json_unlabelled_file)
images = json_unlabelled_load['images']
# info = json_image_load['info']
# categories = json_image_load['categories']
json_unlabelled_file.close()



with open('_annotations.coco.json','r') as labelled_file:
    json_labelled = json.load(labelled_file)

# get the number of labelled dataset, which will be the index
length = len(json_labelled['images'])
print(length)

# I want to append the image information obtained from unlabelled dataset to
# the end of labelled dataset to generate full training set
for i in images:
    # print(i['id'])
    i['id'] += length
    # change the id first
    if (i['id']>=2000):
        # print(i['id'])
        images.remove(i)
json_labelled['images'].extend(images)
labelled_file.close()

json_load = json_labelled
with open ('_annotations.coco.json', 'w') as new_json:
    json.dump(json_load, new_json)
new_json.close()