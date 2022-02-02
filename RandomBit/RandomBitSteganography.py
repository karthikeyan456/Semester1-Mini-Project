from os import name
from signal import raise_signal
import cv2
from PIL import Image
import streamlit as st

def countpixels(fname):
     img=cv2.imread(fname)
     co=0
     for row in img:
         for pix in row:
             co+=1
     return co

def generaterandom(key):#linear generation of the random number 
    a=1
    b=9
    return a*key+b
def randomnumber(n,key):
    l=[]
    i=0
    while i<=n:
         curr_key=generaterandom(key)
         if curr_key not in l:
            l.append(curr_key)
            key=curr_key
         i+=1
            

        
    #l.sort()
    return l



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
    if len(binstr)>((img.shape[0]*img.shape[1]*3)):
        st.error("Small image size.Please encode small data or provide a big image")
    
   
    else:
        st.write("Encoding Image!!!Please Wait.....")
        blen=len(binstr)
        encpos=randomnumber((blen//3)+1,1000)#why you are dividing blen//3 i cannot understand
        ind=0
        c=0
        #pos=encpos[c]
        encoded=[]
        if max(encpos)>=countpixels(fname):
            st.error("Pixels not sufficient.Choose another key.")
            return #why you have stopped with return
        
        #nexpos=encpos[t]
        print(encpos)
        for row in img:
            for pix in row:
                if ind<blen and c in encpos:
                    rval=numtobin(pix[0])
                    pix[0]=int(rval[:-1]+binstr[ind],2)
                    ind+=1
                if ind<blen and c in encpos:
                    gval=numtobin(pix[1])
                    pix[1]=int(gval[:-1]+binstr[ind])
                    ind+=1
                if ind<blen and c in encpos:
                    bval=numtobin(pix[2])
                    pix[2]=int(bval[:-1]+binstr[ind])
                    ind+=1
                if ind>=blen:
                    print("c",c)  
                    break
                c+=1
              





             



        cv2.imwrite("enc.png",img)
        st.write("Image stored in current directory")
def decode(fname):
    st.write("Decoding Image!!!Please Wait....")
    decbin=""
    ans=""
    img=cv2.imread(fname)
    c=0
    key=1000
    pos=generaterandom(key)
    for row in img:
        for pix in row:
            
                if c==pos:
                    r=numtobin(pix[0])
                    g=numtobin(pix[1])
                    b=numtobin(pix[2])
                    decbin=decbin+r[-1]+g[-1]+b[-1]
                    key=pos
                    pos=generaterandom(key)


                c+=1
    all_bytes = [ decbin[i: i+8] for i in range(0, len(decbin), 8) ]
    for i in all_bytes:
        if chr(int(i,2))=="$":
            break
        ans+=chr(int(i,2))
        #if ans[-3:]=="!@#":
           # break
    if ans[0:3]!="!@#":
        st.write("Image not encoded using the software")
    else:  
      st.write("The Hidden Data is ")
      st.write(ans[3:])
    print(ans)
    



    


    

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
          data="!@#"+data+"$@!"
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
