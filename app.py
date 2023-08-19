from flask import Flask, render_template, request, redirect, session
from gensim.models.fasttext import FastText
import pandas as pd
import pickle
import os
import numpy as np
from bs4 import BeautifulSoup
from PIL import Image
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
ImageList=[]


df=pd.DataFrame(columns={'imageLink','Description','MetadataDump'})

app = Flask(__name__)
app.secret_key = os.urandom(16) 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/CaptionView')
def CaptionView():
    return render_template('Caption.html')


@app.route('/CaptionLink', methods=['GET', 'POST'])
def CaptionLink():
    if request.method == 'POST':
        imageLink = request.form['imageLink']
        tempDict={'ImageLink':imageLink,'Description':''}
        with open('blip_model_zero.pkl', 'rb') as f:
            loaded_model = pickle.load(f)

    # Load the processor
        with open('blip_processor_zero.pkl', 'rb') as f:
            loaded_processor = pickle.load(f)


        image2 = Image.open(requests.get(imageLink, stream=True).raw).convert('RGB')

        inputs = loaded_processor(image2, return_tensors="pt",padding=True)

        out = loaded_model.generate(**inputs)
        tempDict['Description']=loaded_processor.decode(out[0], skip_special_tokens=True)

        ImageList.append(tempDict)
    return render_template('Caption.html',ImageList=ImageList)
    
@app.route('/remove-item/<int:index>', methods=['GET'])
def remove_item(index):
    if 0 <= index < len(ImageList):
        del ImageList[index]
    return redirect('/CaptionLink')



@app.route('/SaveCaption/<int:index>', methods=['GET', 'POST'])
def SaveCaption(index):
    if request.method == 'POST':
        ImageLink = request.form['ImageLink']
        Description = request.form['Description']
        MetadData={}
        global df
        df = df.append({'imageLink':ImageLink,'Description':Description,'MetadataDump':MetadData}, ignore_index=True)
        if 0 <= index < len(ImageList):
            del ImageList[index]
        df.to_csv("CaptionDump.csv")
        pass
    return redirect('/CaptionLink')

if __name__ == '__main__':
    app.run(debug=True)