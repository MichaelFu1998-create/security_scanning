def read_markdown(filename):
    """Reads markdown file, converts output and fetches title and meta-data for
    further processing.
    """
    global MD
    # Use utf-8-sig codec to remove BOM if it is present. This is only possible
    # this way prior to feeding the text to the markdown parser (which would
    # also default to pure utf-8)
    with open(filename, 'r', encoding='utf-8-sig') as f:
        text = f.read()

    if MD is None:
        MD = Markdown(extensions=['markdown.extensions.meta',
                                  'markdown.extensions.tables'],
                      output_format='html5')
    else:
        MD.reset()
        # When https://github.com/Python-Markdown/markdown/pull/672
        # will be available, this can be removed.
        MD.Meta = {}

    # Mark HTML with Markup to prevent jinja2 autoescaping
    output = {'description': Markup(MD.convert(text))}

    try:
        meta = MD.Meta.copy()
    except AttributeError:
        pass
    else:
        output['meta'] = meta
        try:
            output['title'] = MD.Meta['title'][0]
        except KeyError:
            pass

    return output