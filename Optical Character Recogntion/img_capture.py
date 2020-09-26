from PIL import Image
import pytesseract
import argparse
import cv2
import time
import os

import numpy as np
import cv2
cap=cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height

path=("img1.avi")
fourcc=cv2.VideoWriter_fourcc(*'XVID')
out=cv2.VideoWriter(path,fourcc,20.0,(640,480))
count=0
while(cap.isOpened()):
    ret,frame=cap.read()
    count+=1
    k = cv2.waitKey(1) & 0xff
    cv2.imshow('frame',frame)
    if k == 27:
        cv2.imwrite('img1.png',frame)       
        break
    elif count>=250: #capture img after 50 secs
        cv2.imwrite("img1.png",frame)
        break

cap.release()
out.release()
cv2.destroyAllWindows()

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",required=False,default="img1.png",
	help="image")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

# load the example image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

cv2.imshow("Image", gray)


# image-processing
if args["preprocess"] == "thresh":
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# make a check to see if median blurring should be done to remove
# noise
elif args["preprocess"] == "blur":
	gray = cv2.medianBlur(gray, 3)

# write the grayscale image to disk as a temporary file 
filename = "{}.png".format(os.getpid())
cv2.imwrite(filename, gray)

# load the image, apply OCR, and then delete the temporary file
mytext = pytesseract.image_to_string(Image.open(filename))
os.remove(filename)
print(mytext)

# show the output images
# cv2.imshow("Image", image)
# cv2.imshow("Output", gray)



