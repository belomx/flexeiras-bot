from skimage import data
from skimage import io
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imsave
import config
import uuid
import tinys3
import os
import sender
import re

conn = tinys3.Connection(config.aws_access_key, config.aws_secret_key, tls=True, endpoint='s3-sa-east-1.amazonaws.com')

def crop_center(img,cropx,cropy):
    y,x = img.shape
    startx = x//2-(cropx//2)
    starty = y//2-(cropy//2)    
    return img[starty:starty+cropy,startx:startx+cropx]

def work(json_body):       
        image_url = json_body['file_url']
        #image_url = "https://pyimagesearch.com/wp-content/uploads/2015/01/opencv_logo.png"
        img = io.imread( image_url )
        A = img.shape[0] / 3.0
        w = 2.0 / img.shape[1]

        shift = lambda x: A * np.sin(2.0*np.pi*x * w)

        for i in range(img.shape[0]):
                img[:,i] = np.roll(img[:,i], int(shift(i)))

        temp_name = str(uuid.uuid4()) + '.jpg'
        filename = temp_name 
        imsave(temp_name, img)
        f = open(temp_name, 'rb')
        conn.upload(filename, f, config.bucket_name)
        file_url = "https://s3-sa-east-1.amazonaws.com/" + \
                        config.bucket_name + "/" + filename
        print file_url
        f.close()     
        os.remove(temp_name)

