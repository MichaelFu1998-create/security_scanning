def add_mdp_includes(topology=None, kwargs=None):
    """Set the mdp *include* key in the *kwargs* dict.

    1. Add the directory containing *topology*.
    2. Add all directories appearing under the key *includes*
    3. Generate a string of the form "-Idir1 -Idir2 ..." that
       is stored under the key *include* (the corresponding
       mdp parameter)

    By default, the directories ``.`` and ``..`` are also added to the
    *include* string for the mdp; when fed into
    :func:`gromacs.cbook.edit_mdp` it will result in a line such as ::

      include = -I. -I.. -I../topology_dir ....

    Note that the user can always override the behaviour by setting
    the *include* keyword herself; in this case this function does
    nothing.

    If no *kwargs* were supplied then a dict is generated with the
    single *include* entry.

    :Arguments:
       *topology* : top filename
          Topology file; the name of the enclosing directory is added
          to the include path (if supplied) [``None``]
       *kwargs* : dict
          Optional dictionary of mdp keywords; will be modified in place.
          If it contains the *includes* keyword with either a single string
          or a list of strings then these paths will be added to the
          include statement.
    :Returns: *kwargs* with the *include* keyword added if it did not
              exist previously; if the keyword already existed, nothing
              happens.

    .. Note:: The *kwargs* dict is **modified in place**. This
              function is a bit of a hack. It might be removed once
              all setup functions become methods in a nice class.
    """
    if kwargs is None:
        kwargs = {}

    include_dirs = ['.', '..']      # should . & .. always be added?
    if topology is not None:
        # half-hack: find additional itps in the same directory as the topology
        topology_dir = os.path.dirname(topology)
        include_dirs.append(topology_dir)

    include_dirs.extend(asiterable(kwargs.pop('includes', [])))  # includes can be a list or a string

    # 1. setdefault: we do nothing if user defined include
    # 2. modify input in place!
    kwargs.setdefault('include', _mdp_include_string(include_dirs))
    return kwargs