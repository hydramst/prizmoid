import streamlit as st

import functools
import os, sys

import PIL.Image
import time
import requests
import glob


from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'


  
hub_handle = 'model/magenta_arbitrary-image-stylization-v1-256_2'
hub_model = hub.load(hub_handle)

def conver_image_to_jpeg():
  pass


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
  style_file_name = st.text_input("Name your style", 'name')
  style_file = st.file_uploader("Please upload an image file or...", type=["jpg","jpeg", "png"])
  if style_file:
    if st.button("Upload"):
      image = PIL.Image.open(style_file)
      rgb_im = image.convert('RGB')
      new_file_name = os.path.join("styles/", style_file_name + '.jpg')
      st.write(new_file_name)
      with open(new_file_name,"wb") as f: 
          f.write(style_file.getbuffer())         
      st.success("Saved File")

def show_gallery_of_styles():
  images_glob = os.listdir("styles/")
  images_glob = [x for x in images_glob if x.endswith(".jpg")]

  for i in range(len(images_glob)):
    cols = st.columns(2)
    cols[0].image("styles/" + images_glob[i], width = 200)
    cols[1].write(images_glob[i].rsplit('.',1)[0])





page = st.sidebar.radio('Choose action', ('upload_style', 'show_styles', 'transfer_style', 'system_info'))

if page == 'upload_style':
  st.header('Upload new style')
  upload_style_image()

if page == 'show_styles':
  st.header('Styles gallery')
  show_gallery_of_styles()



elif page == 'system_info':
  st.write("TF Version: ", tf.__version__)
  st.write("TF Hub version: ", hub.__version__)

  pwd = os.getcwd()
  listing = os.listdir(pwd)
  st.write(listing)




elif page == "transfer_style":

  images_glob = os.listdir("styles/")
  images_glob = set([x for x in images_glob if x.endswith(".jpg")])
  style_img = st.radio('Choose style', images_glob)


  style_image_url = "styles/" + style_img
  original_image_url = st.text_input("Style image from URL", )

  if st.button('Restyle'):
    download_file(original_image_url, "original.jpg")
    st.image("original.jpg")

    content_image = load_img("original.jpg")
    style_image = load_img(style_image_url)

    st.write(original_image_url)
    st.image(style_image)
    # st.write(style_image_url)
    # st.image(style_image)


    # stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

    # final_img = tensor_to_image(stylized_image)


    st.image(final_img)
