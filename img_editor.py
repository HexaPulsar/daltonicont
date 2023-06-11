import fitz
mat = fitz.Matrix(1200 / 72, 1200 / 72)  # sets zoom factor for 1200 dpi
doc = fitz.open("TestColors.pdf")
for page in doc:
    pix = page.get_pixmap(matrix=mat)
    img_filename = "output/page-%04i.png" % page.number
    pix.pil_save(img_filename, format="PNG", dpi=(1200,1200))


