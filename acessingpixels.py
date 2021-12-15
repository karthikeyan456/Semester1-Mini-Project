import cv2
img=cv2.imread("usain.jpg")
rows=img.shape[0]
columns=img.shape[1]
#print(rows,columns)

c=0
for i in range(rows):
    for j in range(columns):
        if i==0 and j==0:
            print(img[i,j])
        c+=1
print(img[0,0])
#print(c)
#print(img.size)