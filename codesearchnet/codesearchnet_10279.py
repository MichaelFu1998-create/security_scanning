def get_meta_image_url(request, image):
    """
    Resize an image for metadata tags, and return an absolute URL to it.
    """
    rendition = image.get_rendition(filter='original')
    return request.build_absolute_uri(rendition.url)