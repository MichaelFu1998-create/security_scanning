def _sbase_notes_dict(sbase, notes):
    """Set SBase notes based on dictionary.

    Parameters
    ----------
    sbase : libsbml.SBase
        SBML object to set notes on
    notes : notes object
        notes information from cobra object
    """
    if notes and len(notes) > 0:
        tokens = ['<html xmlns = "http://www.w3.org/1999/xhtml" >'] + \
            ["<p>{}: {}</p>".format(k, v) for (k, v) in notes.items()] + \
            ["</html>"]
        _check(
            sbase.setNotes("\n".join(tokens)),
            "Setting notes on sbase: {}".format(sbase)
        )