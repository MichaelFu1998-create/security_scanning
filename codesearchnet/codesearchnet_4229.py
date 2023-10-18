def str_from_text(text):
    """
    Return content of a free form text block as a string.
    """
    REGEX = re.compile('<text>((.|\n)+)</text>', re.UNICODE)
    match = REGEX.match(text)
    if match:
        return match.group(1)
    else:
        return None