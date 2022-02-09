import cv2
def countpixels(fname):
     #Function to count the total number of pixels in the image
     img=cv2.imread(fname)
     co=0
     for row in img:
         for pix in row:
             co+=1
     return co
