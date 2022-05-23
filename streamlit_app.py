import streamlit as st
from functions import *
import os

st.set_page_config(
    page_title="PRIZMOID",
    page_icon="🎈",
)

z = 2
types = "jpg", "jpeg", "png"


# 'Screens'
# Upload style image and save file in /styles

def upload_style_image():
    """

    :return:
    """
    style_file_name = st.text_input("Name your style", 'name')
    original_image_url = st.text_input("Please upload style image from URL", )

    if st.button("Upload"):
        style_file = download_file(original_image_url, style_file_name)
        new_file_name = save_new_image_style(style_file, style_file_name)
        st.write(new_file_name)
        st.success("Saved File")


def upload_your_image():
    """

    :return:
    """
    menu = ["Upload", "Web link"]
    choice = st.sidebar.selectbox("Upload/use link", menu)
    if choice == "Upload":
        image_file = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"])
        if image_file:
            st.image(show_image(image_file))
        if st.button('Restyle'):
            file_user_path = save_user_image(image_file)
            content_image = load_img(file_user_path)
            style_image = load_img(style_image_url)
            final_img = transfer_style(content_image, style_image)
            st.image(final_img)
    if choice == "Web link":
        st.write('This feature in progress')
        # original_image_url = st.text_input("Style image from URL", )
        # if st.button('Restyle'):
        #     uploaded_image = download_file(original_image_url, "original.jpg")
        #     st.image(uploaded_image)
        #     content_image = load_img("original.jpg")
        #     style_image = load_img(style_image_url)
        #     final_img = transfer_style(content_image, style_image)
        #     st.image(final_img)


def show_gallery_of_styles():
    """

    :return:
    """
    images_glob = os.listdir("styles/")
    images_glob = [x for x in images_glob if x.endswith(types)]

    for i in range(len(images_glob)):
        cols = st.columns(2)
        cols[0].image("styles/" + images_glob[i], width=200)
        cols[1].write(images_glob[i].rsplit('.', 1)[0])


page = st.sidebar.radio('Choose action',
                        ('transfer_style', 'upload_style'))

if page == 'upload_style':
    st.header('Upload new style')
    upload_style_image()

elif page == "transfer_style":
    images_glob = os.listdir("styles/")
    images_glob = set([x for x in images_glob if x.endswith(types)])
    style_img = st.radio('Choose style', images_glob)
    style_image_url = "styles/" + style_img

    # original_image = upload_your_image()

    upload_your_image()

    #     if st.button('Restyle'):
    #         uploaded_image = download_file(original_image, "original.jpg")
    #         st.image(uploaded_image)
    #         content_image = load_img("original.jpg")
    #         style_image = load_img(style_image_url)
    #         final_img = transfer_style(content_image, style_image)
    #         st.image(final_img)
    # original_image_url = st.text_input("Style image from URL", )
    #
    # if st.button('Restyle'):
    #     uploaded_image = download_file(original_image_url, "original.jpg")
    #     st.image(uploaded_image)
    #     content_image = load_img("original.jpg")
    #     style_image = load_img(style_image_url)
    #     final_img = transfer_style(content_image, style_image)
    #     st.image(final_img)

    st.header('Styles gallery')
    show_gallery_of_styles()

    if st.button('system_info'):
        pwd = os.getcwd()
        listing = os.listdir(pwd)
        st.write(listing)
        st.write(os.listdir(pwd + '/styles/'))
