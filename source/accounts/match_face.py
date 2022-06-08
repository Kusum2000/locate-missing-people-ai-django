import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import imutils
import os
from sklearn import preprocessing
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential
from tensorflow.keras import backend as K
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.pipeline import Pipeline




model = tf.keras.applications.VGG16(
            include_top=True,
            weights="imagenet",
            input_tensor=None,
            input_shape=None,
            pooling=None,
            classes=1000,
            classifier_activation="softmax",
        )


def pcaFuse(layer,pipeline):
    layer=pipeline.fit_transform(layer)
    return layer


def encode_label(missing_labels):
    label_encoder = preprocessing.LabelEncoder()
    labels_dict = dict()
    u_labels=missing_labels
    missing_labels_en= label_encoder.fit_transform(missing_labels)
    for i in range(0,len(missing_labels)):
        if missing_labels_en[i] not in labels_dict:
            labels_dict[missing_labels_en[i]]=missing_labels[i]
            u_labels.append(missing_labels[i])
            #print(missing_labels[i])
    missing_labels_en= label_encoder.fit_transform(u_labels)
    return missing_labels_en,u_labels

def encode_img(missing_labels,aligned_img):
    img = cv2.equalizeHist(cv2.cvtColor(aligned_img, cv2.COLOR_BGR2GRAY))
            
    img= cv2.resize(img,(224,224))
    img2 = cv2.merge((img,img,img))
    img = img_to_array(img2)
    i=np.array([img])
    
    encode = models.Sequential()
    encode.add(model)
    encode.add(layers.Flatten())
    encode.add(layers.Dense(512, activation='relu'))
    encode.add(layers.Dropout(0.5))
    encode.add(layers.Dense(len(set(missing_labels))-1,activation='softmax'))
    predict_img=encode.predict(i)
    return predict_img


def preprocess(path,missing_imgs,missing_labels,aligned_img):
    #labels = np.zeros((1, len(missing_imgs)+1))
    i = 0
    images = []
    missing_labels_en,final_labels_list = encode_label(missing_labels)

    for filename in missing_imgs:
        f=filename.split('/')
        img = cv2.imread(os.path.join(path,f[0],f[1]))
        img= cv2.equalizeHist(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
        
        img= cv2.resize(img,(224,224))
        img2 = cv2.merge((img,img,img))
        img = img_to_array(img2)
        images.append(img2)
        i +=1
    n_labels = len(set(missing_labels_en))
    for i in range(0,n_labels):
        img = cv2.equalizeHist(cv2.cvtColor(aligned_img, cv2.COLOR_BGR2GRAY))
            
        img= cv2.resize(img,(224,224))
        img2 = cv2.merge((img,img,img))
        img = img_to_array(img2)
        images.append(img)
    return np.array(images),missing_labels_en,final_labels_list

def feature_extraction(images,missing_labels_en):

    with tf.device('/device:cpu:0'):
        Flatten_list = [];
        FC7_list = [];
        FC6_list = [];
        l = len(model.layers)
        for i in range(len(images)):
            image = images[i]
            img = image.reshape((1, image.shape[0], image.shape[1], image.shape[2])) 

            keras_function = K.function([model.get_layer(index=0).input], model.get_layer(index=l - 4).output)
            Flatten = keras_function([img])

            keras_function = K.function([model.get_layer(index=0).input], model.get_layer(index=l - 3).output)
            FC7 = keras_function([img])

            keras_function = K.function([model.get_layer(index=0).input], model.get_layer(index=l - 2).output)
            FC6 = keras_function([img])

            
            Flatten_list.append(Flatten[0])
            FC7_list.append(FC7[0])
            FC6_list.append(FC6[0])
    pipeline = Pipeline([('scaling', StandardScaler()), ('pca', PCA(n_components=len(images)))])
    flatten_new=pcaFuse(Flatten_list,pipeline)
    fc7_new=pcaFuse(FC7_list,pipeline)
    fc6_new=pcaFuse(FC7_list,pipeline)    

    return flatten_new,fc7_new,fc6_new, missing_labels_en

def match_faces(encoded_dataset,predict_img,missing_labels):
    min=0
    individual_rank={}
    i=0
    for c in encoded_dataset:
        dist = np.linalg.norm(c-predict_img)
        if missing_labels[i] not in individual_rank:
            individual_rank[missing_labels[i]]=dist
        elif missing_labels[i] in individual_rank:
            individual_rank[missing_labels[i]]+=dist
        #print('Answer',missing_labels[i], dist)     
        i+=1
    print(individual_rank)  
    for k,v in individual_rank.items():
        if v>min :
            min=v
            result=k
    print(result,min)
    return(result,min,individual_rank)