def rle_encode(text, use_bwt=True):
    r"""Perform encoding of run-length-encoding (RLE).

    This is a wrapper for :py:meth:`RLE.encode`.

    Parameters
    ----------
    text : str
        A text string to encode
    use_bwt : bool
        Indicates whether to perform BWT encoding before RLE encoding

    Returns
    -------
    str
        Word decoded by RLE

    Examples
    --------
    >>> rle_encode('align')
    'n\x00ilag'
    >>> rle_encode('align', use_bwt=False)
    'align'

    >>> rle_encode('banana')
    'annb\x00aa'
    >>> rle_encode('banana', use_bwt=False)
    'banana'

    >>> rle_encode('aaabaabababa')
    'ab\x00abbab5a'
    >>> rle_encode('aaabaabababa', False)
    '3abaabababa'

    """
    if use_bwt:
        text = BWT().encode(text)
    return RLE().encode(text)