def create_portable_topology(topol, struct, **kwargs):
    """Create a processed topology.

    The processed (or portable) topology file does not contain any
    ``#include`` statements and hence can be easily copied around. It
    also makes it possible to re-grompp without having any special itp
    files available.

    :Arguments:
      *topol*
          topology file
      *struct*
          coordinat (structure) file

    :Keywords:
      *processed*
          name of the new topology file; if not set then it is named like
          *topol* but with ``pp_`` prepended
      *includes*
          path or list of paths of directories in which itp files are
          searched for
      *grompp_kwargs**
          other options for :program:`grompp` such as ``maxwarn=2`` can
          also be supplied

    :Returns: full path to the processed topology
    """
    _topoldir, _topol = os.path.split(topol)
    processed = kwargs.pop('processed', os.path.join(_topoldir, 'pp_'+_topol))
    grompp_kwargs, mdp_kwargs = filter_grompp_options(**kwargs)
    mdp_kwargs = add_mdp_includes(topol, mdp_kwargs)
    with tempfile.NamedTemporaryFile(suffix='.mdp') as mdp:
        mdp.write('; empty mdp file\ninclude = {include!s}\n'.format(**mdp_kwargs))
        mdp.flush()
        grompp_kwargs['p'] = topol
        grompp_kwargs['pp'] = processed
        grompp_kwargs['f'] =  mdp.name
        grompp_kwargs['c'] = struct
        grompp_kwargs['v'] = False
        try:
            gromacs.grompp(**grompp_kwargs)
        finally:
            utilities.unlink_gmx('topol.tpr', 'mdout.mdp')
    return utilities.realpath(processed)