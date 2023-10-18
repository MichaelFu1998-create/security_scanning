def dequote_docstring(text):
    """Remove the quotes delimiting a docstring."""
    # TODO: Process escaped characters unless raw mode?
    text = text.strip()
    if len(text) > 6 and text[:3] == text[-3:] == '"""':
        # Standard case, """..."""
        return text[3:-3]
    if len(text) > 7 and text[:4] in ('u"""', 'r"""') and text[-3:] == '"""':
        # Unicode, u"""...""", or raw r"""..."""
        return text[4:-3]
    # Other flake8 tools will report atypical quotes:
    if len(text) > 6 and text[:3] == text[-3:] == "'''":
        return text[3:-3]
    if len(text) > 7 and text[:4] in ("u'''", "r'''") and text[-3:] == "'''":
        return text[4:-3]
    if len(text) > 2 and text[0] == text[-1] == '"':
        return text[1:-1]
    if len(text) > 3 and text[:2] in ('u"', 'r"') and text[-1] == '"':
        return text[2:-1]
    if len(text) > 2 and text[0] == text[-1] == "'":
        return text[1:-1]
    if len(text) > 3 and text[:2] in ("u'", "r'") and text[-1] == "'":
        return text[2:-1]
    raise ValueError("Bad quotes!")