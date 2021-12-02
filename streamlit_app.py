import streamlit as st

import functools
import os

from matplotlib import gridspec
import matplotlib.pylab as plt
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub

st.write("TF Version: ", tf.__version__)
st.write("TF Hub version: ", hub.__version__)
st.write("Eager mode enabled: ", tf.executing_eagerly())
st.write("GPU available: ", tf.config.list_physical_devices('GPU'))
