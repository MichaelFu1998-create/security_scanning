def showImage(layout, imagePath="", imageObj=None, offset=(0, 0),
              bgcolor=COLORS.Off, brightness=255):
    """Display an image on the matrix"""
    if not isinstance(layout, Matrix):
        raise RuntimeError("Must use Matrix with showImage!")

    layout.all_off()

    return show_image(layout.set, layout.width, layout.height, imagePath,
                      imageObj, offset, bgcolor, brightness)