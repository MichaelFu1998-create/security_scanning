def img_src_finder(pipeline_index,
                   soup,
                   finder_image_urls=[],
                   *args, **kwargs):
    """
    Find image URL in <img>'s src attribute
    """

    now_finder_image_urls = []

    for img in soup.find_all('img'):
        src = img.get('src', None)
        if src:
            src = str(src)
            if (src not in finder_image_urls) and \
               (src not in now_finder_image_urls):
                now_finder_image_urls.append(src)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output