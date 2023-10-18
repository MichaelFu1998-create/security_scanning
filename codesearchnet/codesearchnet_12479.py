def apply_job_security(code):
    """Treat input `code` like Python 2 (implicit strings are byte literals).

    The implementation is horribly inefficient but the goal is to be compatible
    with what Mercurial does at runtime.
    """
    buf = io.BytesIO(code.encode('utf8'))
    tokens = tokenize.tokenize(buf.readline)
    # NOTE: by setting the fullname to `mercurial.pycompat` below, we're
    # ensuring that hg-specific pycompat imports aren't inserted to the code.
    data = tokenize.untokenize(replacetokens(list(tokens), 'mercurial.pycompat'))
    return cast(str, data.decode('utf8'))