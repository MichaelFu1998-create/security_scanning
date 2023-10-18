def insert_break(lines, break_pos=9):
    """
    Insert a <!--more--> tag for larger release notes.

    Parameters
    ----------
    lines : list of str
        The content of the release note.
    break_pos : int
        Line number before which a break should approximately be inserted.

    Returns
    -------
    list of str
        The text with the inserted tag or no modification if it was
        sufficiently short.
    """
    def line_filter(line):
        if len(line) == 0:
            return True
        return any(line.startswith(c) for c in "-*+")

    if len(lines) <= break_pos:
        return lines
    newlines = [
        i for i, line in enumerate(lines[break_pos:], start=break_pos)
        if line_filter(line.strip())]
    if len(newlines) > 0:
        break_pos = newlines[0]
    lines.insert(break_pos, "<!--more-->\n")
    return lines