def topology(struct=None, protein='protein',
             top='system.top',  dirname='top',
             posres="posres.itp",
             ff="oplsaa", water="tip4p",
             **pdb2gmx_args):
    """Build Gromacs topology files from pdb.

    :Keywords:
       *struct*
           input structure (**required**)
       *protein*
           name of the output files
       *top*
           name of the topology file
       *dirname*
           directory in which the new topology will be stored
       *ff*
           force field (string understood by ``pdb2gmx``); default
           "oplsaa"
       *water*
           water model (string), default "tip4p"
       *pdb2gmxargs*
           other arguments for ``pdb2gmx``

    .. note::
       At the moment this function simply runs ``pdb2gmx`` and uses
       the resulting topology file directly. If you want to create
       more complicated topologies and maybe also use additional itp
       files or make a protein itp file then you will have to do this
       manually.
    """

    structure = realpath(struct)

    new_struct = protein + '.pdb'
    if posres is None:
        posres = protein + '_posres.itp'

    pdb2gmx_args.update({'f': structure, 'o': new_struct, 'p': top, 'i': posres,
                         'ff': ff, 'water': water})

    with in_dir(dirname):
        logger.info("[{dirname!s}] Building topology {top!r} from struct = {struct!r}".format(**vars()))
        # perhaps parse output from pdb2gmx 4.5.x to get the names of the chain itp files?
        gromacs.pdb2gmx(**pdb2gmx_args)
    return { \
            'top': realpath(dirname, top), \
            'struct': realpath(dirname, new_struct), \
            'posres' : realpath(dirname, posres) }