from os import name
import cv2
from PIL import Image
import streamlit as st

def msgtobin(data):
    binstr=""
    for char in data:
        binstr+=format(ord(char),"08b")
    #print(binstr)
    return binstr
def numtobin(num):
    return format(num,"08b")
def encode(fname,data):
    img=cv2.imread(fname)
    print(fname)
    binstr=msgtobin(data)
    print(binstr)
    if len(binstr)>((img.shape[0]*img.shape[1]*3)//16):
        st.error("Small image size.Please encode small data or provide a big image")
   
    else:
        st.write("Encoding Image!!!Please Wait.....")
        blen=len(binstr)
        ind=0
        c=0
        for row in img:
            for pix in row:
                for j in range(3):
                    if c%2==0 and ind<blen:
                        cbin=numtobin(pix[j])
                        pix[j]=int(cbin[:-1]+binstr[ind],2)
                        ind+=1
                    c+=1
        cv2.imwrite("enc.png",img)
        st.write("Image stored in current directory")
def decode(fname):
    st.write("Decoding Image!!!Please Wait....")
    decbin=""
    ans=""
    img=cv2.imread(fname)
    c=0
    for row in img:
        for pix in row:
            for col in pix:
                if c%2==0:
                    cbin=numtobin(col)
                    decbin+=cbin[-1]
                c+=1
    all_bytes = [ decbin[i: i+8] for i in range(0, len(decbin), 8) ]
    for i in all_bytes:
        if chr(int(i,2))=="!":
            break
        ans+=chr(int(i,2))
        #if ans[-3:]=="!@#":
           # break


    st.write("The Hidden Data is ")
    st.write(ans)
    



    


    

def main():
    st.title("Hiding and Recovering Data using Steganography")
    st.markdown("<style>body{background-color:Blue;}</style>",unsafe_allow_html=True)
    operations=["Hide Data","Recover Data"]
    ch=st.radio("Choose the operation you want to perform",operations)
    if ch=="Hide Data":
       st.subheader("Upload Image To Hide Data")
       image_file=st.file_uploader("Upload Images",type=["png","jpeg","jpg"])
       data=st.text_input("Enter data to hide ")
       if len(data)==0:
           st.write("No data enetered")
       #data+="!@#"
       #msgtobin(data)



       if image_file!=None and len(data)!=0:
          st.image(Image.open(image_file),width=250)
          #img=cv2.imread(image_file.name)
          #print(data)
          st.write("Image Uploaded Successfully")
          data+="!@#"
          st.button("Start Encoding",on_click=encode(image_file.name,data))
    else:
       st.subheader("Upload Image To Recover Data")
       image_file=st.file_uploader("Upload Images",type=["png","jpeg","jpg"])
       if image_file!=None:
           st.image(Image.open(image_file),width=250)
           #img=cv2.imread(image_file.name)
           #print(img)
           st.write("Image Uploaded Successfully")
           st.button("Start Decoding",on_click=decode(image_file.name))

main()

    

#st.title("Upload and Display Image")
