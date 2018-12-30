from PIL import Image
from io import StringIO
import PIL
import io
import os
import sys

class Transformio:
    def __init__(self,img):
        self.img = Image.open(img)

    def showFormat(self):
        print(self.img.format)
        self.img.show()

    def tryCompress(self):
        picture = self.img
        dim = picture.size
	
	    #set quality= to the preferred quality. 
	    #I found that 85 has no difference in my 6-10mb files and that 65 is the lowest reasonable number
        picture.save("Compressed.jpg","JPEG",optimize=True,quality=85) 
	
        print("File compressed")

    def changeColor(self):
        greyscale_image = self.img.convert('L')
        greyscale_image.save('greyscale_image.jpg')