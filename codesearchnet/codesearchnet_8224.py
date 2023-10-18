def loadImage(layout, imagePath="", imageObj=None, offset=(0, 0),
              bgcolor=COLORS.Off, brightness=255):
    """Display an image on the matrix"""

    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with loadImage!")

    texture = [[COLORS.Off for x in range(layout.width)]
               for y in range(layout.height)]

    def setter(x, y, pixel):
        if y >= 0 and x >= 0:
            texture[y][x] = pixel

    show_image(setter, layout.width, layout.height, imagePath, imageObj,
               offset, bgcolor, brightness)

    return texture