def __encode_multipart_formdata(self, fields, files):
        """
        fields is a sequence of (key, value) elements for regular form fields.
        files is a sequence of (filename, filehandle) files to be uploaded
        returns (content_type, body)
        """
        BOUNDARY = _make_boundary()

        if len(files) > 0:
            fields['nFileCount'] = str(len(files))

        crlf = '\r\n'
        buf = BytesIO()

        for k, v in fields.items():
            if DEBUG:
                print("field: %s: %s" % (repr(k), repr(v)))
            lines = [
                '--' + BOUNDARY,
                'Content-disposition: form-data; name="%s"' % k,
                '',
                str(v),
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))

        n = 0
        for f, h in files.items():
            n += 1
            lines = [
                '--' + BOUNDARY,
                'Content-disposition: form-data; name="File%d"; '
                'filename="%s"' % (n, f),
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))
            lines = [
                'Content-type: application/octet-stream',
                '',
                '',
            ]
            buf.write(crlf.join(lines).encode('utf-8'))
            buf.write(h.read())
            buf.write(crlf.encode('utf-8'))

        buf.write(('--' + BOUNDARY + '--' + crlf).encode('utf-8'))
        content_type = "multipart/form-data; boundary=%s" % BOUNDARY
        return content_type, buf.getvalue()