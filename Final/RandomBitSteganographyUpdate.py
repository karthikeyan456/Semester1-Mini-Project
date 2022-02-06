
import cv2
from PIL import Image
import streamlit as st
#Import modules required

def countpixels(fname):
     #Function to count the total number of pixels in the image
     img=cv2.imread(fname)
     co=0
     for row in img:
         for pix in row:
             co+=1
     return co

def generaterandom(key):
    #Function to generate the next random number
    a=1
    b=10
    return a*key+b

def randomnumber(n,key):
    #Function to generate a list of random numbers
    l=[]
    i=0
    while i<=n:
         curr_key=generaterandom(key)
         if curr_key not in l:
            l.append(curr_key)
            key=curr_key
         i+=1
            


    return l



def msgtobin(data):
    #Function to convert the message into a binary string
    binstr=""
    for char in data:
        binstr+=format(ord(char),"08b")
    
    return binstr

def numtobin(num):
    #Function to convert number to a binary string
    return format(num,"08b")

def encode(fname,data,key):
    #Function to carry out encoding process
    img=cv2.imread(fname)#Opening the image
    
    binstr=msgtobin(data)#Converting the secret message to it's binary equivalent
    
    if len(binstr)>((img.shape[0]*img.shape[1]*3)):#Checking if image has sufficient pixels to encode the image.
        st.error("Small image size.Please encode small data or provide a big image")
    
   
    else:
        st.write("Encoding Image!!!Please Wait.....")
        blen=len(binstr)
        encpos=randomnumber((blen//3)+1,key)#Generating a list of random numbers.
        ind=0
        c=0
        
        if max(encpos)>=countpixels(fname):#Checking if the there are sufficient random pixels to encode the data
            st.error("Pixels not sufficient.Choose another key.")
            return
        
        
        
        for row in img:#Iterating through rows of an image
            for pix in row:#Iterating through the pixels of a row

                if ind<blen and c in encpos:#Encoding in red value of the pixel
                    rval=numtobin(pix[0])
                    print("R",pix[0])
                    pix[0]=int(rval[:-1]+binstr[ind],2)
                    print("R",pix[0])
                    ind+=1
                
                if ind<blen and c in encpos:#Encoding in the green value of pixel
                    gval=numtobin(pix[1])
                    print("G",pix[1])
                    pix[1]=int(gval[:-1]+binstr[ind],2)
                    print("G",pix[1])
                    ind+=1

                if ind<blen and c in encpos:#Encoding in the blue value of the pixel.
                    bval=numtobin(pix[2])
                    print("B",pix[2])
                    pix[2]=int(bval[:-1]+binstr[ind],2)
                    print("B",pix[2])
                    ind+=1

                if ind>=blen:#Breaking out the loop if all the bits in the binary data are encoded.
                    
                    break

                c+=1
        
              





             
        cv2.imwrite("enc.png",img)#Storing the encoded image in CWD
        st.write("Image stored in current directory")

def decode(fname,key):
    #Function to perform decoding
    st.write("Decoding Image!!!Please Wait....")
    decbin=""#Empty string to store binary equivalent of the encoded data.
    ans=""#Empty string to store the actual encoded data
    img=cv2.imread(fname)#Opening the image file
    c=0
    
    pos=generaterandom(key)#Generating the first random number using the key
    for row in img:#Iterating through rows of an image
        for pix in row:#Iterating through the pixels of a row
            
                if c==pos:
                    r=numtobin(pix[0])
                    g=numtobin(pix[1])
                    b=numtobin(pix[2])
                    decbin=decbin+r[-1]+g[-1]+b[-1]#Extracting LSBs from R,G,B Values of the pixel
                    key=pos
                    pos=generaterandom(key)


                c+=1
    all_bytes = [ decbin[i: i+8] for i in range(0, len(decbin), 8) ]#Split the binary string to get substrings of 8 characters
    for v in range(len(all_bytes)):
        if v<len(all_bytes)-2 and chr(int(all_bytes[v],2))=="$" and chr(int(all_bytes[v+1],2))=="@" and chr(int(all_bytes[v+2],2))=="!":#Breaking out of loop if the special end charcter is found
            break
        ans+=chr(int(all_bytes[v],2))
        
    if ans[0:3]!="!@#":#Checking if the special starting characters are found
        st.write("Image not encoded using the software")
    else:  
      st.write("The Hidden Data is ")#Displayingthe hidden data
      st.write(ans[3:])
    print(ans)
    



    


    

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
          st.button("",on_click=encode(image_file.name,data,int(key)))#Invoking encode function
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
           st.button("",on_click=decode(image_file.name,int(key)))#Invoking Decode function

main()

    


