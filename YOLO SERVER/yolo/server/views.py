from pickle import GET
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import torch
import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from urllib import request
import base64
from io import BytesIO
import json
# Create your views here.
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
def to_data_uri(img):
    data = BytesIO()
    img.save(data, "JPEG") # pick your format
    data64 = base64.b64encode(data.getvalue())
    # return u'data:img/jpeg;base64,'+data64.decode('utf-8') 
    return data64.decode('utf-8') 
def Model():
    # img=request.urlretrieve(url,"image.png")
    img=Image.open("hello_level.jpeg")
    image=np.array(img)
    results=model(img)
    df=results.pandas().xyxy[0]
    xmin=df['xmin'].values.astype('int')
    ymin=df['ymin'].values.astype('int')
    xmax=df['xmax'].values.astype('int')
    ymax=df['ymax'].values.astype('int')
    confidence=(df['confidence'].values*100).astype('int')
    name=df['name'].values
    color = (255, 0, 0)
    thickness = 2
    for i in range(len(xmin)):
        start_point=(int(xmin[i]),int(ymin[i]))
        end_point=(int(xmax[i]),int(ymax[i]))
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        image=cv2.putText(image,str(i+1),(int((xmin[i]+xmax[i])/2),int((ymin[i]+ymax[i])/2)),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),2,cv2.LINE_AA)
    img = Image.fromarray(image, 'RGB')
    img=to_data_uri(img)
    # print(img)
    # with open("hello_level.jpeg", "rb") as image2string:
    #     converted_string = base64.b64encode(image2string.read()).decode("utf-8")

    # return img,xmin,ymin,xmax,ymax,confidence,name,converted_string
    return xmin,ymin,xmax,ymax,confidence,name,img
def detect(request):
    # if request.method == 'POST':
        # url=request.POST.get('url')
        xmin,ymin,xmax,ymax,confidence,name,converted_string = Model()
        
        # params={"image":img, 'xmin':xmin, 'ymin':ymin,'xmax':xmax, 'ymax':ymax,'confidence':confidence,'name':name,'img':converted_string}
        params={ 'xmin':xmin, 'ymin':ymin,'xmax':xmax, 'ymax':ymax,'confidence':confidence,'name':name,'img':converted_string}
        j={}
        for k,v in params.items():
            try:
                j[k]=v.tolist()
            except:
                j[k]=v
        # j = json.dumps({k: v.tolist() for k, v in params.items()})
        
        # return render(request,'index.html',params)
        return JsonResponse(j)
    
    # return render(request,'index.html')

def test_api(request):
    x = {
    "name": "John",
    "age": 30,
    "city": "New York"
    }

    return JsonResponse(x,safe=False)
def Model_test(img_arr):
    results=model(img_arr)
    df=results.pandas().xyxy[0]
    xmin=df['xmin'].values.astype('int')
    ymin=df['ymin'].values.astype('int')
    xmax=df['xmax'].values.astype('int')
    ymax=df['ymax'].values.astype('int')
    confidence=(df['confidence'].values*100).astype('int')
    name=df['name'].values
    color = (255, 0, 0)
    thickness = 2
    for i in range(len(xmin)):
        start_point=(int(xmin[i]),int(ymin[i]))
        end_point=(int(xmax[i]),int(ymax[i]))
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    img = Image.fromarray(image, 'RGB')
    img=to_data_uri(img)
    return img,xmin,ymin,xmax,ymax,confidence,name

def image_decode(request):
    if request.method ==GET:
        img=request.POST.get(img)
        decodeit = open('hello_level.jpeg', 'wb')
        decodeit.write(base64.b64decode((img)))
        decodeit.close()
        img=Image.open(decodeit)
        img_arr=np.array(img)
        image,xmin,ymin,xmax,ymax,confidence,name=Model(img_arr)
        params={'image':image, 'xmin':xmin, 'ymin':ymin,'xmax':xmax, 'ymax':ymax,'confidence':confidence,'name':name}
        return render(request,'index.html',params)
    # decoded_img=base64.b64decode(img)
    # return HttpResponse(decoded_img)

def testing(request):
    print("working!!!")
    if request.method == 'POST':
        print("yes")
        img=request.POST.get('img')
        print("Started writing")
        datafile=open('result.txt','w')
        datafile.write(img)
        datafile.close()
        decodeit = open('hello_level.jpeg', 'wb')
        decodeit.write(base64.b64decode((img)))
        decodeit.close()
        print("Done writing")
        return HttpResponse(img)

