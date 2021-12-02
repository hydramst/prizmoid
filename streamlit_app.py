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


  
  
hub_handle = 'model/arbitrary-image-stylization-v1-256/2'
hub_module = hub.load(hub_handle)

content_image = "https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/Golden_Gate_Bridge_from_Battery_Spencer.jpg/640px-Golden_Gate_Bridge_from_Battery_Spencer.jpg"
style_image = "https://upload.wikimedia.org/wikipedia/commons/0/0a/The_Great_Wave_off_Kanagawa.jpg"

outputs = hub_module(tf.constant(content_image), tf.constant(style_image))
stylized_image = outputs[0]
