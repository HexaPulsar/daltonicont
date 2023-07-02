''' 
OCR MODULE
See https://ocrmypdf.readthedocs.io/en/latest/installation.html
to install, in windows it required chocolatey
For now the files gets heavier xdxxdxdxddddd
TODO: !!!! ESTUDIAR LA LIBRERIA, SE SUPONE QUE PUEDE DEJAR MENOS PESADOS LOS ARCHIVOS
'''
# Import libraries
# Se necesita unpaper
import ocrmypdf
# Basic execution
#                                         lo deje aqui owo
# ocrmypdf.configure_logging()
# , deskew=True
ocrmypdf.ocr('output\\pdf\\archivo.pdf', 'output\\pdf\\OCR_output.pdf', output_type = "pdf", optimize = 1)