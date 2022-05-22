import tensorflow as tf
import numpy as np
import PIL.Image
import os
import requests
import tensorflow_hub as hub

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

hub_handle = 'model/magenta_arbitrary-image-stylization-v1-256_2'
hub_model = hub.load(hub_handle)


def load_img(path_to_img: str):
    """

    :param path_to_img:
    :return:
    """
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
    """

    :param tensor:
    :return:
    """
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def save_new_image_style(style_file, style_file_name):
    """

    :param style_file:
    :param style_file_name:
    :return:
    """
    image = PIL.Image.open(style_file)
    rgb_im = image.convert('RGB')
    new_file_name = os.path.join("styles/", style_file_name + '.jpg')
    rgb_im.save(new_file_name, format="JPEG")
    return new_file_name


def download_file(url, local_filename):
    """

    :param url:
    :param local_filename:
    :return:
    """
    r = requests.get(url)
    f = open(local_filename, 'wb')
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:  # filter out keep-alive new chunks
            f.write(chunk)
    f.close()
    return local_filename


def transfer_style(content_image, style_image):
    """

    :param content_image:
    :param style_image:
    :return:
    """
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    final_img = tensor_to_image(stylized_image)
    return final_img
