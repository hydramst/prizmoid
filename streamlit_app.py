import streamlit as st

import functools
import os

import PIL.Image
import time


from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'


st.write("TF Version: ", tf.__version__)
st.write("TF Hub version: ", hub.__version__)
st.write("Eager mode enabled: ", tf.executing_eagerly())
st.write("GPU available: ", tf.config.list_physical_devices('GPU'))


  
  
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


def tensor_to_image(tensor):
  tensor = tensor*255
  tensor = np.array(tensor, dtype=np.uint8)
  if np.ndim(tensor)>3:
    assert tensor.shape[0] == 1
    tensor = tensor[0]
  return PIL.Image.fromarray(tensor)


original_image = st.text_input("Original image URL",)
style_image = st.text_input("Style image from URL", )

if st.button('Restyle'):

  content_path = tf.keras.utils.get_file('from.jpg',original_image)
  style_path = tf.keras.utils.get_file('to.jpg', style_image)

  content_image = load_img(content_path)
  style_image = load_img(style_path)

  st.write(original_image)
  st.image(content_path)
  st.write(style_image)
  st.image(style_image)


  stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]

  final_img = tensor_to_image(stylized_image)


  st.image(final_img)
