def deparagraph(element, doc):
    """Panflute filter function that converts content wrapped in a Para to
    Plain.

    Use this filter with pandoc as::

        pandoc [..] --filter=lsstprojectmeta-deparagraph

    Only lone paragraphs are affected. Para elements with siblings (like a
    second Para) are left unaffected.

    This filter is useful for processing strings like titles or author names so
    that the output isn't wrapped in paragraph tags. For example, without
    this filter, pandoc converts a string ``"The title"`` to
    ``<p>The title</p>`` in HTML. These ``<p>`` tags aren't useful if you
    intend to put the title text in ``<h1>`` tags using your own templating
    system.
    """
    if isinstance(element, Para):
        # Check if siblings exist; don't process the paragraph in that case.
        if element.next is not None:
            return element
        elif element.prev is not None:
            return element

        # Remove the Para wrapper from the lone paragraph.
        # `Plain` is a container that isn't rendered as a paragraph.
        return Plain(*element.content)