def a_href_finder(pipeline_index,
                  soup,
                  finder_image_urls=[],
                  *args, **kwargs):
    """
    Find image URL in <a>'s href attribute
    """

    now_finder_image_urls = []

    for a in soup.find_all('a'):
        href = a.get('href', None)
        if href:
            href = str(href)
            if filter(href.lower().endswith, ('.jpg', '.jpeg', '.gif', '.png')):
              if (href not in finder_image_urls) and \
                 (href not in now_finder_image_urls):
                    now_finder_image_urls.append(href)

    output = {}
    output['finder_image_urls'] = finder_image_urls + now_finder_image_urls

    return output