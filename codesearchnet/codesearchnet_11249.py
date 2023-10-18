def rle_decode(text, use_bwt=True):
    r"""Perform decoding of run-length-encoding (RLE).

    This is a wrapper for :py:meth:`RLE.decode`.

    Parameters
    ----------
    text : str
        A text string to decode
    use_bwt : bool
        Indicates whether to perform BWT decoding after RLE decoding

    Returns
    -------
    str
        Word decoded by RLE

    Examples
    --------
    >>> rle_decode('n\x00ilag')
    'align'
    >>> rle_decode('align', use_bwt=False)
    'align'

    >>> rle_decode('annb\x00aa')
    'banana'
    >>> rle_decode('banana', use_bwt=False)
    'banana'

    >>> rle_decode('ab\x00abbab5a')
    'aaabaabababa'
    >>> rle_decode('3abaabababa', False)
    'aaabaabababa'

    """
    text = RLE().decode(text)
    if use_bwt:
        text = BWT().decode(text)
    return text