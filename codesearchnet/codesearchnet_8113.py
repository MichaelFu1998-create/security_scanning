def crop(image, top_offset=0, left_offset=0, bottom_offset=0, right_offset=0):
    """Return an image cropped on top, bottom, left or right."""
    if bottom_offset or top_offset or left_offset or right_offset:
        width, height = image.size
        box = (left_offset, top_offset,
               width - right_offset, height - bottom_offset)
        image = image.crop(box=box)

    return image