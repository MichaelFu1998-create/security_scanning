def openany(datasource, mode='rt', reset=True):
    """Context manager for :func:`anyopen`.

    Open the `datasource` and close it when the context of the :keyword:`with`
    statement exits.

    `datasource` can be a filename or a stream (see :func:`isstream`). A stream
    is reset to its start if possible (via :meth:`~io.IOBase.seek` or
    :meth:`~cString.StringIO.reset`).

    The advantage of this function is that very different input sources
    ("streams") can be used for a "file", ranging from files on disk (including
    compressed files) to open file objects to sockets and strings---as long as
    they have a file-like interface.

    :Arguments:
      *datasource*
           a file or a stream
      *mode*
           {'r', 'w'} (optional), open in r(ead) or w(rite) mode
      *reset*
           bool (optional) try to read (`mode` 'r') the stream from the
           start [``True``]


    **Example**

    Open a gzipped file and process it line by line::

        with openany("input.pdb.gz") as pdb:
            for line in pdb:
                if line.startswith('ATOM'):
                    print(line)

    Open a URL and read it::

       import urllib2
       with openany(urllib2.urlopen("https://www.mdanalysis.org/")) as html:
           print(html.read())


    .. SeeAlso::
       :func:`anyopen`

    """
    stream = anyopen(datasource, mode=mode, reset=reset)
    try:
        yield stream
    finally:
        stream.close()