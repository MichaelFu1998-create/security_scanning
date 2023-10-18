def convert_lsstdoc_tex(
        content, to_fmt, deparagraph=False, mathjax=False,
        smart=True, extra_args=None):
    """Convert lsstdoc-class LaTeX to another markup format.

    This function is a thin wrapper around `convert_text` that automatically
    includes common lsstdoc LaTeX macros.

    Parameters
    ----------
    content : `str`
        Original content.

    to_fmt : `str`
        Output format for the content (see https://pandoc.org/MANUAL.html).
        For example, 'html5'.

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
    augmented_content = '\n'.join((LSSTDOC_MACROS, content))
    return convert_text(
        augmented_content, 'latex', to_fmt,
        deparagraph=deparagraph, mathjax=mathjax,
        smart=smart, extra_args=extra_args)