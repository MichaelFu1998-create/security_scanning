def sentencecase(string):
    """Convert string into sentence case.
    First letter capped and each punctuations are joined with space.

    Args:
        string: String to convert.

    Returns:
        string: Sentence cased string.

    """
    joiner = ' '
    string = re.sub(r"[\-_\.\s]", joiner, str(string))
    if not string:
        return string
    return capitalcase(trimcase(
        re.sub(r"[A-Z]", lambda matched: joiner +
                                         lowercase(matched.group(0)), string)
    ))