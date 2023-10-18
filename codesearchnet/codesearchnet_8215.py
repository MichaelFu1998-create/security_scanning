def image_to_colorlist(image, container=list):
    """Given a PIL.Image, returns a ColorList of its pixels."""
    deprecated.deprecated('util.gif.image_to_colorlist')

    return container(convert_mode(image).getdata())