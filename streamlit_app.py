import streamlit as st

import functools
import os

import PIL.Image
import time
import requests


from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'


st.write("TF Version: ", tf.__version__)
st.write("TF Hub version: ", hub.__version__)

  
  
hub_handle = 'model/magenta_arbitrary-image-stylization-v1-256_2'
hub_model = hub.load(hub_handle)


def load_img(path_to_img):
  max_dim = 512
  img = tf.io.read_file(path_to_img)
  img = tf.image.decode_image(img, channels=3)
  img = tf.image.convert_image_dtype(img, tf.float32)

  shape = tf.cast(tf.shape(img)[:-1], tf.float32)
  long_dim = max(shape)
  scale = max_dim / long_dim

  new_shape = tf.cast(shape * scale, tf.int32)

  img = tf.image.resize(img, new_shape)
  img = img[tf.newaxis, :]
  return img


def download_file(url, local_filename):
    r = requests.get(url)
    f = open(local_filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024): 
        if chunk: # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    return 



def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)


### 'Screens'

## Upload style image and save file in /styles

def upload_style_image():
  st.title("Upload image for styling")


pwd = os.getcwd()
listing = os.listdir(pwd)
st.write(listing)

page = st.sidebar.radio('Choose action', ('upload_style', 'transfer_style', 'system_info'))

if page == 'upload_style':
  st.header('Upload new style')
  style_file = st.file_uploader("Please upload an image file or...", type=["jpg","jpeg", "png"])
  if style_file:
    with open(os.path.join("styles",style_file.name),"wb") as f: 
        f.write(image_file.getbuffer())         
    st.success("Saved File")



elif page == "transfer_style":
    




  original_image_url = st.text_input("Original image URL",)
  style_image_url = st.text_input("Style image from URL", )

  if st.button('Restyle'):
    download_file(original_image_url, "original.jpg")
    download_file(style_image_url, "style.jpg")
    #content_path = tf.keras.utils.get_file('from.jpg',original_image_url)
    #style_path = tf.keras.utils.get_file('to.jpg', style_image_url)

    content_image = load_img("original.jpg")
    style_image = load_img("style.jpg")

    st.write(original_image_url)
    #st.image(content_image)
    # st.write(style_image_url)
    # st.image(style_image)


    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    final_img = tensor_to_image(stylized_image)


    st.image(final_img)
