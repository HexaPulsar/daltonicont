class struct_image:
  def __init__(self,image) -> None:
    self.ext = image["ext"]
    self.smask = image["smask"]
    self.height = image["height"]
    self.width = image["width"]
    self.cs = image["colorspace"]
    self.cs_name = image["cs-name"]
    self.xres = image["xres"]
    self.yres = image["yres"]
    self.image = image["image"]


