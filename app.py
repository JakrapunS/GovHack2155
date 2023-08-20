from flask import Flask, render_template, request, redirect, session
from gensim.models.fasttext import FastText
import pandas as pd
import pickle
import os
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image
import requests
import numpy 
from transformers import BlipProcessor, BlipForConditionalGeneration
ImageList=[]
ImageList_PVOA=[]
import csv
from data_collection import * 



# loaded_processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
# loaded_model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large")



app = Flask(__name__)
app.secret_key = os.urandom(16) 



with open('blip_model_zero.pkl', 'rb') as f:
                loaded_model = pickle.load(f)

with open('blip_processor_zero.pkl', 'rb') as f:
        loaded_processor = pickle.load(f)
        
with open('blip_model_vqa.pkl', 'rb') as f:
    loaded_model_vqa = pickle.load(f)

# Load the processor
with open('blip_processor_vqa.pkl', 'rb') as f:
    loaded_processor_vqa = pickle.load(f)


def tag_generate(img_url,model_vqa,processor_vqa, q_num):
  tag=set()
   
  raw_image = Image.open(requests.get(img_url, stream=True).raw).convert('RGB')

  if q_num >=1 :
    # Question 9
    question_9 = "Is there people in the image?"
    inputs = processor_vqa(raw_image, question_9, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    result = processor_vqa.decode(out[0], skip_special_tokens=True)
    if result == 'yes':
      tag.add('human')
      tag.add('people')

  if q_num >=2 :
    # Question 2
    question_2 = "What is the setting of the image?"
    inputs = processor_vqa(raw_image, question_2, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))
    
  if q_num >=3 :
    # Question 8
    question_8 = "What is the context on image?"
    inputs = processor_vqa(raw_image, question_8, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))
    

  if q_num >=4 :
    # Question 4
    question_4 = "What is the image all about?"
    inputs = processor_vqa(raw_image, question_4, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))
   
  if q_num >=5 :
    # Question 3
    question_3 = "What is the objects of the image?"
    inputs = processor_vqa(raw_image, question_3, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))
    
  if q_num >=6 :
    # Question 1
    question_1 = "What is the color of the photo?"
    inputs = processor_vqa(raw_image, question_1, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))
    
  if q_num >=7 :
    # Question 10
    question_10 = "Is there animal in the image?"
    inputs = processor_vqa(raw_image, question_10, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    result = processor_vqa.decode(out[0], skip_special_tokens=True)
    if result == 'yes':
      tag.add('animal')
  if q_num >=8 :
    # Question 11
    question_11 = "Is there building in the image?"
    inputs = processor_vqa(raw_image, question_11, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    result = processor_vqa.decode(out[0], skip_special_tokens=True)
    if result == 'yes':
      tag.add('building')
     

  if q_num >=9 :
    # Question 5
    question_5 = "What is the cultural or geographics context of the image?"
    inputs = processor_vqa(raw_image, question_5, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))

  if q_num >=10 :
    # Question 6
    question_6 = "What is the overall composition of the image?"
    inputs = processor_vqa(raw_image, question_6, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))

  if q_num >=11 :
    # Question 7
    question_7 = "What decade the image come from?"
    inputs = processor_vqa(raw_image, question_7, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    tag.add(processor_vqa.decode(out[0], skip_special_tokens=True))

  if q_num >=12 :
    # Question 12
    question_12 = "Is there vehical in the image?"
    inputs = processor_vqa(raw_image, question_12, return_tensors="pt")
    out = model_vqa.generate(**inputs)
    result = processor_vqa.decode(out[0], skip_special_tokens=True)
    if result == 'yes':
      tag.add('vehical')

  tag.discard("none")

  return tag

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CaptionView')
def CaptionView():
    return render_template('Caption.html',ImageList=ImageList)


@app.route('/CaptionPVOAView')
def CaptionPVOAView():
    return render_template('captionPVOA.html',ImageList=ImageList_PVOA)


@app.route('/CaptionLink', methods=['GET', 'POST'])
def CaptionLink():
    global loaded_processor
    global loaded_model
    
    global loaded_model_vqa
    global loaded_processor_vqa
    if request.method == 'POST':
        imageLink = request.form['imageLink']
        tags=tag_generate(imageLink,loaded_model_vqa,loaded_processor_vqa,5)
        tempDict={'ImageLink':imageLink,'Description':'','tags':list(tags)}
        


        image2 = Image.open(requests.get(imageLink, stream=True).raw).convert('RGB')

        inputs = loaded_processor(image2, return_tensors="pt")

        out = loaded_model.generate(**inputs)
        description=loaded_processor.decode(out[0], skip_special_tokens=True)
        
        tempDict['Description']=description.replace("arafed","")

        ImageList.append(tempDict)
    return render_template('Caption.html',ImageList=ImageList)



@app.route('/PVOA_Series_IMAGE', methods=['GET', 'POST'])
def PVOA_Series_IMAGE():
    global loaded_processor
    global loaded_model
    global loaded_model_vqa
    global loaded_processor_vqa
    if request.method == 'POST':
        # SeriesID = request.form['SeriesID']
        keyword=request.form['keyword']
        try:
            keyword=int(keyword) ## It is serious
        except:
            pass
            

        actualData=make_data(keyword)
        actualData=actualData.sample(n=5)
       

        for index, row in actualData.iterrows():
            tags=tag_generate(row['link'],loaded_model_vqa,loaded_processor_vqa,5)
            print(tags)
            tempDict={'ImageLink':row['link'],'Description':'','old_Desc':row['description'],'tags':list(tags),'archive_link':row['archive_link']}
            print(row['archive_link'])

        # Load the processor
            

            image2 = Image.open(requests.get(row['link'], stream=True).raw).convert('RGB')

            inputs = loaded_processor(image2, return_tensors="pt")

            out = loaded_model.generate(**inputs)
            description=loaded_processor.decode(out[0], skip_special_tokens=True)
            
            tempDict['Description']=description.replace("arafed","")

            ImageList_PVOA.append(tempDict)
    return render_template('captionPVOA.html',ImageList=ImageList_PVOA)


    
@app.route('/remove-item/<int:index>', methods=['GET'])
def remove_item(index):
    if 0 <= index < len(ImageList):
        del ImageList[index]
    return redirect('/CaptionLink')


@app.route('/remove-item-PVOA/<int:index>', methods=['GET'])
def remove_item_PVOA(index):
    if 0 <= index < len(ImageList_PVOA):
        del ImageList_PVOA[index]
    return redirect('/PVOA_Series_IMAGE')


@app.route('/SaveCaption/<int:index>', methods=['GET', 'POST'])
def SaveCaption(index):
    if request.method == 'POST':
      
        ImageLink = request.form['ImageLink']
        Description = request.form['Description']
        MetadData = request.form['tags']
    
        
        
        temp={'imageLink':ImageLink,'Description':Description,'MetadataDump':MetadData}

        
        with open('CaptionDump.csv', mode='a', newline='') as csv_file:
            # Create DictWriter object
            field_names=['imageLink','Description','MetadataDump']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            
            # Write the dictionary to CSV
            writer.writerow(temp)


        if 0 <= index < len(ImageList):
            del ImageList[index]
    return redirect('/CaptionLink')


@app.route('/SaveCaption-PVOA/<int:index>', methods=['GET', 'POST'])
def SaveCaption_PVOA(index):
    if request.method == 'POST':
      
        ImageLink = request.form['ImageLink']
        Description = request.form['Description']
        MetadData = request.form['tags']

        


        
        
        temp={'imageLink':ImageLink,'Description':Description,'MetadataDump':MetadData}

        
        with open('CaptionDump.csv', mode='a', newline='') as csv_file:
            # Create DictWriter object
            field_names=['imageLink','Description','MetadataDump']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            
            # Write the dictionary to CSV
            writer.writerow(temp)


        if 0 <= index < len(ImageList_PVOA):
            del ImageList_PVOA[index]
    return redirect('/PVOA_Series_IMAGE')


if __name__ == '__main__':
    app.run(debug=True)