def make_main_index(struct, selection='"Protein"', ndx='main.ndx', oldndx=None):
    """Make index file with the special groups.

    This routine adds the group __main__ and the group __environment__
    to the end of the index file. __main__ contains what the user
    defines as the *central* and *most important* parts of the
    system. __environment__ is everything else.

    The template mdp file, for instance, uses these two groups for T-coupling.

    These groups are mainly useful if the default groups "Protein" and "Non-Protein"
    are not appropriate. By using symbolic names such as __main__ one
    can keep scripts more general.

    :Returns:
      *groups* is a list of dictionaries that describe the index groups. See
      :func:`gromacs.cbook.parse_ndxlist` for details.

    :Arguments:
      *struct* : filename
        structure (tpr, pdb, gro)
      *selection* : string
        is a ``make_ndx`` command such as ``"Protein"`` or ``r DRG`` which
        determines what is considered the main group for centering etc. It is
        passed directly to ``make_ndx``.
      *ndx* : string
         name of the final index file
      *oldndx* : string
         name of index file that should be used as a basis; if None
         then the ``make_ndx`` default groups are used.

    This routine is very dumb at the moment; maybe some heuristics will be
    added later as could be other symbolic groups such as __membrane__.
    """

    logger.info("Building the main index file {ndx!r}...".format(**vars()))

    # pass 1: select
    # get a list of groups
    # need the first "" to get make_ndx to spit out the group list.
    _,out,_ = gromacs.make_ndx(f=struct, n=oldndx, o=ndx, stdout=False,
                                      input=("", "q"))
    groups = cbook.parse_ndxlist(out)

    # find the matching groups,
    # there is a nasty bug in GROMACS where make_ndx may have multiple
    # groups, which caused the previous approach to fail big time.
    # this is a work around the make_ndx bug.
    # striping the "" allows compatibility with existing make_ndx selection commands.
    selection = selection.strip("\"")

    selected_groups = [g for g in groups if g['name'].lower() == selection.lower()]

    if len(selected_groups) > 1:
        logging.warn("make_ndx created duplicated groups, performing work around")

    if len(selected_groups) <= 0:
        msg = "no groups found for selection {0}, available groups are {1}".format(selection, groups)
        logging.error(msg)
        raise ValueError(msg)

    # Found at least one matching group, we're OK

    # index of last group
    last = len(groups) - 1
    assert last == groups[-1]['nr']

    group = selected_groups[0]

    # pass 2:
    # 1) last group is __main__
    # 2) __environment__ is everything else (eg SOL, ions, ...)
    _,out,_ = gromacs.make_ndx(f=struct, n=ndx, o=ndx,
                                      stdout=False,
                                             # make copy selected group, this now has index last + 1
                                      input=("{0}".format(group['nr']),
                                             # rename this to __main__
                                             "name {0} __main__".format(last+1),
                                             # make a complement to this group, it get index last + 2
                                             "! \"__main__\"",
                                             # rename this to __environment__
                                             "name {0} __environment__".format(last+2),
                                             # list the groups
                                             "",
                                             # quit
                                             "q"))
    return cbook.parse_ndxlist(out)