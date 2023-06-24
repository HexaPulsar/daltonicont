''' 
OCR MODULE
See https://ocrmypdf.readthedocs.io/en/latest/installation.html
to install, in windows it required chocolatey
For now the files gets heavier xdxxdxdxddddd
TODO: !!!! ESTUDIAR LA LIBRERIA, SE SUPONE QUE PUEDE DEJAR MENOS PESADOS LOS ARCHIVOS
'''
# Import libraries
import ocrmypdf
# Basic execution
#                                         lo deje aqui owo
ocrmypdf.ocr('output\\pdf\\archivo.pdf', 'output\\pdf\\OCR_output.pdf', deskew=True)