def save(url, *args, **kwargs):
    """ Parse the options, set defaults and then fire up PhantomJS. """

    device = heimdallDevice(kwargs.get('device', None))

    kwargs['width'] = kwargs.get('width', None) or device.width
    kwargs['height'] = kwargs.get('height', None) or device.height
    kwargs['user_agent'] = kwargs.get('user_agent', None) or device.user_agent

    screenshot_image = screenshot(url, **kwargs)

    if kwargs.get('optimize'):
        image = Image.open(screenshot_image.path)
        image.save(screenshot_image.path, optimize=True)

    return screenshot_image