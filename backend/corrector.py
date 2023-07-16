'''
Modulo final de correción de colores B&W
'''
# Importado de librerías
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
import sys

# Definición de funciones
# (Todas asumen que ya está abierta la imagen)

## Binarización B&W (preprocesado)
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

## PLACEHOLDER DE FILTRO DALTONISMO!!!!!!!!! MODIFICAR
## Filtro de cambio de color 
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

## Reniversión de B&W
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

if __name__ == "__main__":
  



  print("ola")
  # probar con  resources/img/metro_example.png
  # Igual si u.u
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

