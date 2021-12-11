import cv2
from PIL import Image
import streamlit
streamlit.title("Upload and Display Image")
streamlit.subheader("Upload Image")
image_file=streamlit.file_uploader("Upload Images",type=["png","jpeg","jpg"])
if image_file!=None:
    streamlit.image(Image.open(image_file),width=250)
    streamlit.write("Image Uploaded Successfully")