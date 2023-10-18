def pypi_render(source):
    """
    Copied (and slightly adapted) from pypi.description_tools
    """
    ALLOWED_SCHEMES = '''file ftp gopher hdl http https imap mailto mms news
        nntp prospero rsync rtsp rtspu sftp shttp sip sips snews svn svn+ssh
        telnet wais irc'''.split()

    settings_overrides = {
        "raw_enabled": 0,  # no raw HTML code
        "file_insertion_enabled": 0,  # no file/URL access
        "halt_level": 2,  # at warnings or errors, raise an exception
        "report_level": 5,  # never report problems with the reST code
    }

    # capture publishing errors, they go to stderr
    old_stderr = sys.stderr
    sys.stderr = s = StringIO.StringIO()
    parts = None

    try:
        # Convert reStructuredText to HTML using Docutils.
        document = publish_doctree(source=source,
            settings_overrides=settings_overrides)

        for node in document.traverse():
            if node.tagname == '#text':
                continue
            if node.hasattr('refuri'):
                uri = node['refuri']
            elif node.hasattr('uri'):
                uri = node['uri']
            else:
                continue
            o = urlparse.urlparse(uri)
            if o.scheme not in ALLOWED_SCHEMES:
                raise TransformError('link scheme not allowed')

        # now turn the transformed document into HTML
        reader = readers.doctree.Reader(parser_name='null')
        pub = Publisher(reader, source=io.DocTreeInput(document),
            destination_class=io.StringOutput)
        pub.set_writer('html')
        pub.process_programmatic_settings(None, settings_overrides, None)
        pub.set_destination(None, None)
        pub.publish()
        parts = pub.writer.parts

    except:
        pass

    sys.stderr = old_stderr

    # original text if publishing errors occur
    if parts is None or len(s.getvalue()) > 0:
        return None
    else:
        return parts['body']