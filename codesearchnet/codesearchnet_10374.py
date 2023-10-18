def isstream(obj):
    """Detect if `obj` is a stream.

    We consider anything a stream that has the methods

    - ``close()``

    and either set of the following

    - ``read()``, ``readline()``, ``readlines()``
    - ``write()``, ``writeline()``, ``writelines()``

    :Arguments:
      *obj*
          stream or str

    :Returns:
      *bool*, ``True`` if `obj` is a stream, ``False`` otherwise

    .. SeeAlso::
       :mod:`io`


    .. versionadded:: 0.7.1
    """
    signature_methods = ("close",)
    alternative_methods = (
        ("read", "readline", "readlines"),
        ("write", "writeline", "writelines"))

    # Must have ALL the signature methods
    for m in signature_methods:
        if not hasmethod(obj, m):
            return False
    # Must have at least one complete set of alternative_methods
    alternative_results = [
        numpy.all([hasmethod(obj, m) for m in alternatives])
        for alternatives in alternative_methods]
    return numpy.any(alternative_results)