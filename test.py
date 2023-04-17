#extract images from pdf in python 
import fitz
import io
import os
from PIL import Image 
import matplotlib.pyplot as plt
from clases import *
# STEP 2
# file path you want to extract images from
file = "pdf_test/Ishihara_Tests.pdf"
  
# open the file
pdf_file = fitz.open(file)
  
# STEP 3
# iterate over PDF pages
for page_index in range(len(pdf_file)):
  
    # get the page itself
    page = pdf_file[page_index]
    
    image_list = page.get_images()
    
    # printing number of images found in this page
    if image_list:
        print(
            f"[+] Found a total of {len(image_list)} images in page {page_index}")
    else:
        print("[!] No images found on page", page_index)
    for image_index, img in enumerate(page.get_images(), start=1):
        # get the XREF of the image
        xref = img[0]
        base_image = pdf_file.extract_image(xref)
        image_bytes = base_image["image"]
        # get the image extension
        image_ext = base_image["ext"]

        
        # load it to PIL
        image_name = str(image_index) + '.' + image_ext
        #Save image

        images_path = "daltonicont/extraction/extractinpage"+str(image_index)+str(page_index)
        
        valid_ext = ['jpg', 'jpeg', 'png']
        if image_ext in valid_ext:
            try:
                if not os.path.exists(images_path):
                    os.makedirs(images_path)
            except:
                print("creating directory" + images_path)

            with open(os.path.join(images_path, image_name) , 'wb') as image_file:
                image_file.write(image_bytes)
                image_file.close()
            print("image saved!")


def pdf_to_png():
  for page in pdf_file:
      pix = page.get_pixmap(matrix=fitz.Identity, dpi=None,
                            colorspace=fitz.csRGB, clip=None, alpha=False, annots=True)
      pix.save("samplepdfimage-%i.jpg" % page.number)  # save file

      