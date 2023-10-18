def convert_text(content, from_fmt, to_fmt, deparagraph=False, mathjax=False,
                 smart=True, extra_args=None):
    """Convert text from one markup format to another using pandoc.

    This function is a thin wrapper around `pypandoc.convert_text`.

    Parameters
    ----------
    content : `str`
        Original content.

    from_fmt : `str`
        Format of the original ``content``. Format identifier must be one of
        those known by Pandoc. See https://pandoc.org/MANUAL.html for details.

    to_fmt : `str`
        Output format for the content.

    deparagraph : `bool`, optional
        If `True`, then the
        `lsstprojectmeta.pandoc.filters.deparagraph.deparagraph` filter is
        used to remove paragraph (``<p>``, for example) tags around a single
        paragraph of content. That filter does not affect content that
        consists of multiple blocks (several paragraphs, or lists, for
        example). Default is `False`.

        For example, **without** this filter Pandoc will convert
        the string ``"Title text"`` to ``"<p>Title text</p>"`` in HTML. The
        paragraph tags aren't useful if you intend to wrap the converted
        content in different tags, like ``<h1>``, using your own templating
        system.

        **With** this filter, Pandoc will convert the string ``"Title text"``
        to ``"Title text"`` in HTML.

    mathjax : `bool`, optional
        If `True` then Pandoc will markup output content to work with MathJax.
        Default is False.

    smart : `bool`, optional
        If `True` (default) then ascii characters will be converted to unicode
        characters like smart quotes and em dashes.

    extra_args : `list`, optional
        Sequence of Pandoc arguments command line arguments (such as
        ``'--normalize'``). The ``deparagraph``, ``mathjax``, and ``smart``
        arguments are convenience arguments that are equivalent to items
        in ``extra_args``.

    Returns
    -------
    output : `str`
        Content in the output (``to_fmt``) format.

    Notes
    -----
    This function will automatically install Pandoc if it is not available.
    See `ensure_pandoc`.
    """
    logger = logging.getLogger(__name__)

    if extra_args is not None:
        extra_args = list(extra_args)
    else:
        extra_args = []

    if mathjax:
        extra_args.append('--mathjax')

    if smart:
        extra_args.append('--smart')

    if deparagraph:
        extra_args.append('--filter=lsstprojectmeta-deparagraph')

    extra_args.append('--wrap=none')

    # de-dupe extra args
    extra_args = set(extra_args)

    logger.debug('Running pandoc from %s to %s with extra_args %s',
                 from_fmt, to_fmt, extra_args)

    output = pypandoc.convert_text(content, to_fmt, format=from_fmt,
                                   extra_args=extra_args)
    return output