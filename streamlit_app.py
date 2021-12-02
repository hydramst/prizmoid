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
hub_module = hub.load(hub_handle)


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



content_path = tf.keras.utils.get_file('YellowLabradorLooking_new.jpg', 'https://storage.googleapis.com/download.tensorflow.org/example_images/YellowLabradorLooking_new.jpg')
style_path = tf.keras.utils.get_file('kandinsky5.jpg','https://storage.googleapis.com/download.tensorflow.org/example_images/Vassily_Kandinsky%2C_1913_-_Composition_7.jpg')


content_image = load_img(content_path)
style_image = load_img(style_path)


outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
stylized_image = outputs[0]
