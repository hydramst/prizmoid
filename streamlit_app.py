import streamlit as st
from functions import *
import os


st.set_page_config(
    page_title="PRIZMOID",
    page_icon="🎈",
)


z = 2

# 'Screens'
# Upload style image and save file in /styles

def upload_style_image():
    style_file_name = st.text_input("Name your style", 'name')
    style_file = st.file_uploader("Please upload an image file or...", type=["jpg", "jpeg", "png"])
    if style_file:
        if st.button("Upload"):
            new_file_name = save_new_image_style(style_file, style_file_name)
            st.write(new_file_name)
            st.success("Saved File")


def show_gallery_of_styles():
    images_glob = os.listdir("styles/")
    images_glob = [x for x in images_glob if x.endswith(".jpg")]

    for i in range(len(images_glob)):
        cols = st.columns(2)
        cols[0].image("styles/" + images_glob[i], width=200)
        cols[1].write(images_glob[i].rsplit('.', 1)[0])


page = st.sidebar.radio('Choose action', ('upload_style', 'show_styles', 'transfer_style', 'system_info'))

if page == 'upload_style':
    st.header('Upload new style')
    upload_style_image()

if page == 'show_styles':
    st.header('Styles gallery')
    show_gallery_of_styles()

elif page == 'system_info':
    pwd = os.getcwd()
    listing = os.listdir(pwd)
    st.write(listing)
    st.write(os.listdir(pwd + '/styles/'))

elif page == "transfer_style":
    images_glob = os.listdir("styles/")
    images_glob = set([x for x in images_glob if x.endswith(".jpg")])
    style_img = st.radio('Choose style', images_glob)
    style_image_url = "styles/" + style_img
    original_image_url = st.text_input("Style image from URL", )

    if st.button('Restyle'):
        uploaded_image = download_file(original_image_url, "original.jpg")
        st.image(uploaded_image)
        content_image = load_img("original.jpg")
        style_image = load_img(style_image_url)
        final_img = transfer_style(content_image, style_image)
        st.image(final_img)
