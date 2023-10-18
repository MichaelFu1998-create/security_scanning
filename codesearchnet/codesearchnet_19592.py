def imsize(fname):
    """
    return image size (height, width)
    :param fname:
    :return:
    """
    from PIL import Image
    im = Image.open(fname)
    return im.size[1], im.size[0]