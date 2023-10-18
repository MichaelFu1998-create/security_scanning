def screenshot(url, *args, **kwargs):
    """ Call PhantomJS with the specified flags and options. """

    phantomscript = os.path.join(os.path.dirname(__file__),
                                 'take_screenshot.js')

    directory = kwargs.get('save_dir', '/tmp')
    image_name = kwargs.get('image_name', None) or _image_name_from_url(url)
    ext = kwargs.get('format', 'png').lower()
    save_path = os.path.join(directory, image_name) + '.' + ext
    crop_to_visible = kwargs.get('crop_to_visible', False)

    cmd_args = [
        'phantomjs',
        '--ssl-protocol=any',
        phantomscript,
        url,
        '--width',
        str(kwargs['width']),
        '--height',
        str(kwargs['height']),
        '--useragent',
        str(kwargs['user_agent']),
        '--dir',
        directory,
        '--ext',
        ext,
        '--name',
        str(image_name),
    ]
    if crop_to_visible:
        cmd_args.append('--croptovisible')

    # TODO:
    # - quality
    # - renderafter
    # - maxexecutiontime
    # - resourcetimeout

    output = subprocess.Popen(cmd_args,
                              stdout=subprocess.PIPE).communicate()[0]

    return Screenshot(save_path, directory, image_name + '.' + ext, ext)