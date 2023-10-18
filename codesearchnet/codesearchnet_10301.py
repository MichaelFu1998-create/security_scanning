def edit_txt(filename, substitutions, newname=None):
    """Primitive text file stream editor.

    This function can be used to edit free-form text files such as the
    topology file. By default it does an **in-place edit** of
    *filename*. If *newname* is supplied then the edited
    file is written to *newname*.

    :Arguments:
       *filename*
           input text file
       *substitutions*
           substitution commands (see below for format)
       *newname*
           output filename; if ``None`` then *filename* is changed in
           place [``None``]

    *substitutions* is a list of triplets; the first two elements are regular
    expression strings, the last is the substitution value. It mimics
    ``sed`` search and replace. The rules for *substitutions*:

    .. productionlist::
       substitutions: "[" search_replace_tuple, ... "]"
       search_replace_tuple: "(" line_match_RE "," search_RE "," replacement ")"
       line_match_RE: regular expression that selects the line (uses match)
       search_RE: regular expression that is searched in the line
       replacement: replacement string for search_RE

    Running :func:`edit_txt` does pretty much what a simple ::

         sed /line_match_RE/s/search_RE/replacement/

    with repeated substitution commands does.

    Special replacement values:
    - ``None``: the rule is ignored
    - ``False``: the line is deleted (even if other rules match)

    .. note::

       * No sanity checks are performed and the substitutions must be supplied
         exactly as shown.
       * All substitutions are applied to a line; thus the order of the substitution
         commands may matter when one substitution generates a match for a subsequent rule.
       * If replacement is set to ``None`` then the whole expression is ignored and
         whatever is in the template is used. To unset values you must provided an
         empty string or similar.
       * Delete a matching line if replacement=``False``.
    """
    if newname is None:
        newname = filename

    # No sanity checks (figure out later how to give decent diagnostics).
    # Filter out any rules that have None in replacement.
    _substitutions = [{'lRE': re.compile(str(lRE)),
                       'sRE': re.compile(str(sRE)),
                       'repl': repl}
                      for lRE,sRE,repl in substitutions if repl is not None]

    with tempfile.TemporaryFile() as target:
        with open(filename, 'rb') as src:
            logger.info("editing txt = {0!r} ({1:d} substitutions)".format(filename, len(substitutions)))
            for line in src:
                line = line.decode("utf-8")
                keep_line = True
                for subst in _substitutions:
                    m = subst['lRE'].match(line)
                    if m:              # apply substition to this line?
                        logger.debug('match:    '+line.rstrip())
                        if subst['repl'] is False:   # special rule: delete line
                            keep_line = False
                        else:                        # standard replacement
                            line = subst['sRE'].sub(str(subst['repl']), line)
                            logger.debug('replaced: '+line.rstrip())
                if keep_line:
                    target.write(line.encode('utf-8'))
                else:
                    logger.debug("Deleting line %r", line)

        target.seek(0)
        with open(newname, 'wb') as final:
            shutil.copyfileobj(target, final)
    logger.info("edited txt = {newname!r}".format(**vars()))