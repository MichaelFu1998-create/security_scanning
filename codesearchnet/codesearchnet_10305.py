def parse_ndxlist(output):
    """Parse output from make_ndx to build list of index groups::

      groups = parse_ndxlist(output)

    output should be the standard output from ``make_ndx``, e.g.::

       rc,output,junk = gromacs.make_ndx(..., input=('', 'q'), stdout=False, stderr=True)

    (or simply use

       rc,output,junk = cbook.make_ndx_captured(...)

    which presets input, stdout and stderr; of course input can be overriden.)

    :Returns:
       The function returns a list of dicts (``groups``) with fields

       name
           name of the groups
       nr
           number of the group (starts at 0)
       natoms
           number of atoms in the group

    """

    m = NDXLIST.search(output)    # make sure we pick up a proper full list
    grouplist = m.group('LIST')
    return parse_groups(grouplist)