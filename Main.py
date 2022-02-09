import cv2
from PIL import Image
import streamlit as st
from module import decode, encode
def main():
    st.title("Hiding and Recovering Data using Steganography")#Title widget to display title of the page

    operations=["Hide Data","Recover Data"]
    ch=st.radio("Choose the operation you want to perform",operations)#Radio button widget to choose operation

    if ch=="Hide Data":
       st.subheader("Upload Image To Hide Data")

       image_file=st.file_uploader("Upload Images",type=["png","jpeg","jpg"])#File uploader widget to upload images.

       data=st.text_input("Enter data to hide ")#Text input widget to get the message and key as input
       key=st.text_input("Enter key(integer) ")

       if len(data)==0 or len(key)==0:
           st.write("No key or data enetered")
       
       try:
           k=int(key)
       except:#Checking if key is an integer
           st.error("Key must be an integer")
           return



       if image_file!=None and len(data)!=0 and len(key)!=0:
          st.image(Image.open(image_file),width=250)
          
          st.write("Image Uploaded Successfully")
          data="!@#"+data+"$@!"#Appending and prepending special characters to the data
          st.button("",on_click=encode.encode(image_file.name,data,int(key)))#Invoking encode function
    else:
       st.subheader("Upload Image To Recover Data")
       image_file=st.file_uploader("Upload Images",type=["png","jpeg","jpg"])#File uploader widget to upload images.
       key=st.text_input("Enter key(integer) ")#Text widget to get key as input
       if len(key)==0:
           st.write("No key enetered")


       if image_file!=None and len(key)!=0:
           st.image(Image.open(image_file),width=250)
           
           try:
               k=int(key)#Checking for validity of key
           except:
               st.error("Key must be an integer")
               return
           st.write("Image Uploaded Successfully")
           st.button("",on_click=decode.decode(image_file.name,int(key)))#Invoking Decode function

main()
