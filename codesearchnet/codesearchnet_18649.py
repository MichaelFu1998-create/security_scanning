def git_static_file(filename,
                    mimetype='auto',
                    download=False,
                    charset='UTF-8'):
    """ This method is derived from bottle.static_file:

        Open [a file] and return :exc:`HTTPResponse` with status
        code 200, 305, 403 or 404. The ``Content-Type``, ``Content-Encoding``,
        ``Content-Length`` and ``Last-Modified`` headers are set if possible.
        Special support for ``If-Modified-Since`` [...].

        :param filename: Name or path of the file to send.
        :param mimetype: Defines the content-type header (default: guess from
            file extension)
        :param download: If True, ask the browser to open a `Save as...` dialog
            instead of opening the file with the associated program. You can
            specify a custom filename as a string. If not specified, the
            original filename is used (default: False).
        :param charset: The charset to use for files with a ``text/*``
            mime-type. (default: UTF-8)
    """

    # root = os.path.abspath(root) + os.sep
    # filename = os.path.abspath(pathjoin(root, filename.strip('/\\')))
    filename = filename.strip('/\\')
    headers = dict()

    FS = request.app.config['pgs.FS']
    # if not filename.startswith(root):
    #    return HTTPError(403, "Access denied.")
    if not FS.exists(filename):
        return HTTPError(404, "Not found.")
    # if not os.access(filename, os.R_OK):
    # return HTTPError(403, "You do not have permission to access this file.")

    if mimetype == 'auto':
        if download and download is not True:
            mimetype, encoding = mimetypes.guess_type(download)
        else:
            mimetype, encoding = mimetypes.guess_type(filename)
        if encoding:
            headers['Content-Encoding'] = encoding

    if mimetype:
        if mimetype[:5] == 'text/' and charset and 'charset' not in mimetype:
            mimetype += '; charset=%s' % charset
        headers['Content-Type'] = mimetype

    if download:
        download = os.path.basename(filename if download else download)
        headers['Content-Disposition'] = 'attachment; filename="%s"' % download

    # stats = os.stat(filename)
    info = FS.getinfo(filename)
    headers['Content-Length'] = clen = info['size']
    lm = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                       time.gmtime(info['modified_time']))
    headers['Last-Modified'] = lm

    ims = request.environ.get('HTTP_IF_MODIFIED_SINCE')
    if ims:
        ims = parse_date(ims.split(";")[0].strip())
    mtime = info['modified_time']
    if mtime and ims is not None and ims >= int(mtime):
        headers['Date'] = time.strftime("%a, %d %b %Y %H:%M:%S GMT",
                                        time.gmtime())
        return HTTPResponse(status=304, **headers)

    body = '' if request.method == 'HEAD' else FS.get_fileobj(filename)

    clen
    # headers["Accept-Ranges"] = "bytes"
    # ranges = request.environ.get('HTTP_RANGE')
    # if 'HTTP_RANGE' in request.environ:
    #    ranges = list(parse_range_header(request.environ['HTTP_RANGE'], clen))
    #     if not ranges:
    #         return HTTPError(416, "Requested Range Not Satisfiable")
    #    offset, end = ranges[0]
    #    headers["Content-Range"] = "bytes %d-%d/%d" % (offset, end - 1, clen)
    #    headers["Content-Length"] = str(end - offset)
    #    if body: body = _file_iter_range(body, offset, end - offset)
    #     return HTTPResponse(body, status=206, **headers)
    return HTTPResponse(body, **headers)