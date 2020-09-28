# import the necessary packages
from PIL import Image
import pytesseract
import argparse
import cv2
import time
import os

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image",required="True",help="image") 	
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
#cv2.imshow("Image", image)
#cv2.imshow("Output", gray)



