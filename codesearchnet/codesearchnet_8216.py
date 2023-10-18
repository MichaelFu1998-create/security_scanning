def animated_gif_to_colorlists(image, container=list):
    """
    Given an animated GIF, return a list with a colorlist for each frame.
    """
    deprecated.deprecated('util.gif.animated_gif_to_colorlists')

    from PIL import ImageSequence

    it = ImageSequence.Iterator(image)
    return [image_to_colorlist(i, container) for i in it]