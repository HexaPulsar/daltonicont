import fitz
from tqdm import tqdm
from PIL import Image
from skimage.io import imread_collection
import glob
from fpdf import FPDF

def pdf_to_png(doc_path, dpi, output):
    mat = fitz.Matrix(dpi / 72, dpi / 72)  # sets zoom factor for 1200 dpi
    doc = fitz.open(doc_path)
    #todo: agregar try exception
    for page in tqdm(doc):
        pix = page.get_pixmap(matrix=mat)
        img_filename  = output+"/images/page-%04i.png" % page.number
        pix.pil_save(img_filename, format="PNG", dpi=(dpi,dpi))


def png_to_pdf(imgs_path, output_path,encoding = 'RGB'):
    pdf = FPDF()

    path_images = glob.glob(imgs_path+'\\page-*.png') 
    #print(path_images)
   # images_for_pdf = []
   #for image in tqdm(path_images):
      #  img_open = Image.open(image)
      #  img_convert = img_open.convert(encoding)
      #  images_for_pdf.append(img_convert)
       # img_convert.save(imgs_path+'\\archivo.pdf')
    for image in path_images:
        pdf.add_page()
        pdf.image(image,0,0,210,297) #dimensiones de una pagina a4 estandar
    
    pdf.output(output_path+'\\archivo.pdf')


#RUNTIMEEE#

pdf_to_png('pdf_test\TestColors.pdf',1200,'output')
png_to_pdf('output\images',output_path='output\pdf')
