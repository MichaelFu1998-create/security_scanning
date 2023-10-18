def truncate(text, max_len=350, end='...'):
    """Truncate the supplied text for display.

    Arguments:
      text (:py:class:`str`): The text to truncate.
      max_len (:py:class:`int`, optional): The maximum length of the
        text before truncation (defaults to 350 characters).
      end (:py:class:`str`, optional): The ending to use to show that
        the text was truncated (defaults to ``'...'``).

    Returns:
      :py:class:`str`: The truncated text.

    """
    if len(text) <= max_len:
        return text
    return text[:max_len].rsplit(' ', maxsplit=1)[0] + end