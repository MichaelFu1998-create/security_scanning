def edit_mdp(mdp, new_mdp=None, extend_parameters=None, **substitutions):
    """Change values in a Gromacs mdp file.

    Parameters and values are supplied as substitutions, eg ``nsteps=1000``.

    By default the template mdp file is **overwritten in place**.

    If a parameter does not exist in the template then it cannot be substituted
    and the parameter/value pair is returned. The user has to check the
    returned list in order to make sure that everything worked as expected. At
    the moment it is not possible to automatically append the new values to the
    mdp file because of ambiguities when having to replace dashes in parameter
    names with underscores (see the notes below on dashes/underscores).

    If a parameter is set to the value ``None`` then it will be ignored.

    :Arguments:
        *mdp* : filename
            filename of input (and output filename of ``new_mdp=None``)
        *new_mdp* : filename
            filename of alternative output mdp file [None]
        *extend_parameters* : string or list of strings
            single parameter or list of parameters for which the new values
            should be appended to the existing value in the mdp file. This
            makes mostly sense for a single parameter, namely 'include', which
            is set as the default. Set to ``[]`` to disable. ['include']
        *substitutions*
            parameter=value pairs, where parameter is defined by the Gromacs
            mdp file; dashes in parameter names have to be replaced by
            underscores. If a value is a list-like object then the items are
            written as a sequence, joined with spaces, e.g. ::

               ref_t=[310,310,310] --->  ref_t = 310 310 310

    :Returns:
        Dict of parameters that have *not* been substituted.

    **Example** ::

       edit_mdp('md.mdp', new_mdp='long_md.mdp', nsteps=100000, nstxtcout=1000, lincs_iter=2)

    .. Note::

       * Dashes in Gromacs mdp parameters have to be replaced by an underscore
         when supplied as python keyword arguments (a limitation of python). For example
         the MDP syntax is  ``lincs-iter = 4`` but the corresponding  keyword would be
         ``lincs_iter = 4``.
       * If the keyword is set as a dict key, eg ``mdp_params['lincs-iter']=4`` then one
         does not have to substitute.
       * Parameters *aa_bb* and *aa-bb* are considered the same (although this should
         not be a problem in practice because there are no mdp parameters that only
         differ by a underscore).
       * This code is more compact in ``Perl`` as one can use ``s///`` operators:
         ``s/^(\s*${key}\s*=\s*).*/$1${val}/``

    .. SeeAlso:: One can also load the mdp file with
                :class:`gromacs.formats.MDP`, edit the object (a dict), and save it again.
    """
    if new_mdp is None:
        new_mdp = mdp
    if extend_parameters is None:
        extend_parameters = ['include']
    else:
        extend_parameters = list(asiterable(extend_parameters))

    # None parameters should be ignored (simple way to keep the template defaults)
    substitutions = {k: v for k,v in substitutions.items() if v is not None}

    params = list(substitutions.keys())   # list will be reduced for each match

    def demangled(p):
        """Return a RE string that matches the parameter."""
        return p.replace('_', '[-_]')  # must catch either - or _

    patterns = {parameter:
                      re.compile("""\
                       (?P<assignment>\s*{0!s}\s*=\s*)  # parameter == everything before the value
                       (?P<value>[^;]*)              # value (stop before comment=;)
                       (?P<comment>\s*;.*)?          # optional comment
                       """.format(demangled(parameter)), re.VERBOSE)
                     for parameter in substitutions}

    with tempfile.TemporaryFile() as target:
        with open(mdp, 'rb') as src:
            logger.info("editing mdp = {0!r}: {1!r}".format(mdp, substitutions.keys()))
            for line in src:
                line = line.decode('utf-8')
                new_line = line.strip()  # \n must be stripped to ensure that new line is built without break
                for p in params[:]:
                    m = patterns[p].match(new_line)
                    if m:
                        # I am too stupid to replace a specific region in the string so I rebuild it
                        # (matching a line and then replacing value requires TWO re calls)
                        #print 'line:' + new_line
                        #print m.groupdict()
                        if m.group('comment') is None:
                            comment = ''
                        else:
                            comment = " "+m.group('comment')
                        assignment = m.group('assignment')
                        if not assignment.endswith(' '):
                            assignment += ' '
                        # build new line piece-wise:
                        new_line = assignment
                        if p in extend_parameters:
                            # keep original value and add new stuff at end
                            new_line += str(m.group('value')) + ' '
                        # automatically transform lists into space-separated string values
                        value = " ".join(map(str, asiterable(substitutions[p])))
                        new_line += value + comment
                        params.remove(p)
                        break
                target.write((new_line+'\n').encode('utf-8'))
        target.seek(0)
        # XXX: Is there a danger of corrupting the original mdp if something went wrong?
        with open(new_mdp, 'wb') as final:
            shutil.copyfileobj(target, final)

     # return all parameters that have NOT been substituted
    if len(params) > 0:
        logger.warn("Not substituted in {new_mdp!r}: {params!r}".format(**vars()))
    return {p: substitutions[p] for p in params}