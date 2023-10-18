def create_canvas(src, format=None, outputfile=None, multifile=False, buff=None, window=False, title=None,
                  fullscreen=None, show_vars=False):
    """
    Create canvas and sink for attachment to a bot

    canvas is what draws images, 'sink' is the final consumer of the images

    :param src: Defaults for title or outputfile if not specified.

    :param format: CairoImageSink image format, if using buff instead of outputfile
    :param buff: CairoImageSink buffer object to send output to

    :param outputfile: CairoImageSink output filename e.g. "hello.svg"
    :param multifile: CairoImageSink if True,

    :param title: ShoebotWindow - set window title
    :param fullscreen: ShoebotWindow - set window title
    :param show_vars: ShoebotWindow - display variable window

    Two kinds of sink are provided: CairoImageSink and ShoebotWindow

    ShoebotWindow

    Displays a window to draw shoebot inside.


    CairoImageSink

    Output to a filename (or files if multifile is set), or a buffer object.
    """
    from core import CairoCanvas, CairoImageSink # https://github.com/shoebot/shoebot/issues/206

    if outputfile:
        sink = CairoImageSink(outputfile, format, multifile, buff)
    elif window or show_vars:
        from gui import ShoebotWindow
        if not title:
            if src and os.path.isfile(src):
                title = os.path.splitext(os.path.basename(src))[0] + ' - Shoebot'
            else:
                title = 'Untitled - Shoebot'
        sink = ShoebotWindow(title, show_vars, fullscreen=fullscreen)
    else:
        if src and isinstance(src, cairo.Surface):
            outputfile = src
            format = 'surface'
        elif src and os.path.isfile(src):
            outputfile = os.path.splitext(os.path.basename(src))[0] + '.' + (format or 'svg')
        else:
            outputfile = 'output.svg'
        sink = CairoImageSink(outputfile, format, multifile, buff)
    canvas = CairoCanvas(sink)

    return canvas