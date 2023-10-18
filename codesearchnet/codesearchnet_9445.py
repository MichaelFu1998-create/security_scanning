def _image_name_from_url(url):
    """ Create a nice image name from the url. """

    find = r'https?://|[^\w]'
    replace = '_'
    return re.sub(find, replace, url).strip('_')