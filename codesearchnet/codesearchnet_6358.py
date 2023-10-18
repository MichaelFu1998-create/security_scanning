def _parse_notes_dict(sbase):
    """ Creates dictionary of COBRA notes.

    Parameters
    ----------
    sbase : libsbml.SBase

    Returns
    -------
    dict of notes
    """
    notes = sbase.getNotesString()
    if notes and len(notes) > 0:
        pattern = r"<p>\s*(\w+\s*\w*)\s*:\s*([\w|\s]+)<"
        matches = re.findall(pattern, notes)
        d = {k.strip(): v.strip() for (k, v) in matches}
        return {k: v for k, v in d.items() if len(v) > 0}
    else:
        return {}