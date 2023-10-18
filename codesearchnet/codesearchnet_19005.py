def ggpht_s1600_extender(pipeline_index,
                         finder_image_urls,
                         extender_image_urls=[],
                         *args, **kwargs):
    """
    Example:
    http://lh4.ggpht.com/-fFi-qJRuxeY/UjwHSOTHGOI/AAAAAAAArgE/SWTMT-hXzB4/s640/Celeber-ru-Emma-Watson-Net-A-Porter-The-Edit-Magazine-Photoshoot-2013-01.jpg
    to
    http://lh4.ggpht.com/-fFi-qJRuxeY/UjwHSOTHGOI/AAAAAAAArgE/SWTMT-hXzB4/s1600/Celeber-ru-Emma-Watson-Net-A-Porter-The-Edit-Magazine-Photoshoot-2013-01.jpg
    """

    now_extender_image_urls = []

    search_re = re.compile(r'/s\d+/', re.IGNORECASE)

    for image_url in finder_image_urls:
        if 'ggpht.com/' in image_url.lower():
            if search_re.search(image_url):
                extender_image_url = search_re.sub('/s1600/', image_url)
                now_extender_image_urls.append(extender_image_url)

    output = {}
    output['extender_image_urls'] = extender_image_urls + now_extender_image_urls

    return output