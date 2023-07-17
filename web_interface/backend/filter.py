'''
Complete backend code for color transformation in PDF files
for colorblind users

Created by:
Fernanda Borja
Magdalena De La Fuente 
Martin Reyes
Diego Torreblanca
'''
## Global Variables
DPI = 300

## Libraries
import fitz
from fpdf import FPDF 
from tqdm import tqdm
from PIL import Image 
import numpy as np 
import glob
import os
from backend import colorblind_library_copy
# import colorblind_library_copy
import ocrmypdf
from matplotlib import pyplot as plt

'''
File Transformation functions
'''
## PDF file -> PNG images

def pdf_to_png(doc_path, dpi, output, debug = False):
    mat = fitz.Matrix(dpi / 72, dpi / 72)  # sets zoom factor for 1200 dpi
    doc = fitz.open(doc_path)
    #todo: agregar try exception
    for page in tqdm(doc):
        pix = page.get_pixmap(matrix=mat)
        img_filename  = output+"/page-%04i.png" % page.number
        if debug:
            print(f"Converted page {page} into {img_filename}")
        pix.pil_save(img_filename, format="PNG", dpi=(dpi,dpi))

## PNG images -> PDF file
def png_to_pdf(imgs_path, output_path, encoding = 'RGB'):
    pdf = FPDF()

    path_images = glob.glob(imgs_path+'\\filtered-*.png')  
    for image in path_images:
        pdf.add_page()
        pdf.image(image,0,0,210,297) #dimensiones de una pagina a4 estandar
    
    pdf.output(output_path+f'\\filtrado.pdf')


'''
Pixel color transformations
'''
## Binary transformation for Black & White 
# (thresholds needed)
def bwBin(img, upper, lower):
  imgcpy = img.copy()
  for i in range(0, imgcpy.size[0] - 1):
    for j in range(0, imgcpy.size[1] - 1):
      pixel = imgcpy.getpixel((i,j))
      red    = pixel[0]
      green  = pixel[1]
      blue   = pixel[2]
      equal = (red == green == blue)
      if (equal):
        if (red > upper):
          red    = 255
          green  = 255
          blue   = 255
          # superponemos
          imgcpy.putpixel((i, j), (red, green, blue))
        elif (red<lower):
          red    = 0
          green  = 0
          blue   = 0
          # superponemos
          imgcpy.putpixel((i, j), (red, green, blue))
  return imgcpy 

## Testing filter (negative effect)
def negImg(img):
  imgcpy = img.copy()
  for i in range(0, imgcpy.size[0] - 1):
    for j in range(0, imgcpy.size[1] - 1):
        # Sacamos los pixeles
        pixelColorVals = imgcpy.getpixel((i,j))
        # Invertimos
        red    = 255 - pixelColorVals[0]
        green  = 255 - pixelColorVals[1]
        blue   = 255 - pixelColorVals[2]
        # superponemos
        imgcpy.putpixel((i, j), (red, green, blue))
  return imgcpy

## Invert only B&W pixels
def bwinv(img):
  imgcpy = img.copy()
  for i in range(0, imgcpy.size[0] - 1):
    for j in range(0, imgcpy.size[1] - 1):
      pixel = imgcpy.getpixel((i,j))
      red    = pixel[0]
      green  = pixel[1]
      blue   = pixel[2]
      equal = (red == green == blue)
      if (equal and ((red == 255) or (red == 0))):
        red    = 255 - red
        green  = 255 - green
        blue   = 255 - blue
          # superponemos
        imgcpy.putpixel((i, j), (red, green, blue))
  return imgcpy

'''
Full pipeline execution
'''
def full_pipeline(str_list:list):
    filters = str_list 
    pdf_to_png(os.path.join(os.getcwd(),'web_interface' ,'static', 'files','archivo.pdf'), DPI, os.path.join(os.getcwd(), 'output','images','original_png'), debug = False)
    
    list_dir = os.listdir(os.path.join(os.getcwd(), 'output','images','original_png'))
    print(list_dir)
    i = 0
    for image in tqdm(list_dir):
        img = Image.open(f"output\images\original_png\{image}")
        img_bin = bwBin(img, 180, 30)

        correction = colorblind_library_copy.hsv_color_correct(np.asarray(img_bin), colorblind_type=filters[0])
        correction -=1
        # plt.imshow(correction)
        # plt.show()

        # 680-350
        img_inv = bwBin(Image.fromarray(correction), 180, 20)
        img_inv = bwinv(img_inv)

        # plt.imshow(img_inv)
        # plt.show()

        img_inv.save(os.path.join(os.getcwd(), 'output', 'images', 'filtered_png', f'filtered-{i}.png'))  
        i+=1
    # png_to_pdf(os.path.join(os.getcwd(), 'output','images','filtered_png'), os.path.join(os.getcwd(), 'web_interface','static','files'), encoding = 'RGB')
    # ocrmypdf.ocr((os.path.join(os.getcwd(), 'web_interface','static','files','filtrado.pdf')), (os.path.join(os.getcwd(), 'web_interface','static','files','filtrado.pdf')), output_type = "pdf", optimize = 1)
    png_to_pdf(os.path.join(os.getcwd(), 'output','images','filtered_png'), os.path.join(os.getcwd(), 'output','files'), encoding = 'RGB')
    ocrmypdf.ocr((os.path.join(os.getcwd(), 'output','files', 'filtrado.pdf')), (os.path.join(os.getcwd(), 'web_interface','static','files','filtrado.pdf')), output_type = "pdf")



# full_pipeline(['tritanopia'])
"""
if __name__ == "__main__":
 
  imgdir = sys.argv[1]
  img = Image.open(imgdir)
  #
  imgplot = plt.imshow(img)
  plt.show()
  #
  binary = bwBin(img, 180, 30)
  plt.imshow(binary)
  plt.show()
  #
  negative = negImg(binary)
  negimgplot = plt.imshow(negative)
  plt.show()
  #
  invbw = bwinv(negative)
  plt.imshow(invbw)
  plt.show()
"""