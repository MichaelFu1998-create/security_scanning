def add_cmds_cpdir(cpdir,
                   cmdpkl,
                   cpfileglob='checkplot*.pkl*',
                   require_cmd_magcolor=True,
                   save_cmd_pngs=False):
    '''This adds CMDs for each object in cpdir.

    Parameters
    ----------

    cpdir : list of str
        This is the directory to search for checkplot pickles.

    cmdpkl : str
        This is the filename of the CMD pickle created previously.

    cpfileglob : str
        The UNIX fileglob to use when searching for checkplot pickles to operate
        on.

    require_cmd_magcolor : bool
        If this is True, a CMD plot will not be made if the color and mag keys
        required by the CMD are not present or are nan in each checkplot's
        objectinfo dict.

    save_cmd_pngs : bool
        If this is True, then will save the CMD plots that were generated and
        added back to the checkplotdict as PNGs to the same directory as
        `cpx`.

    Returns
    -------

    Nothing.

    '''

    cplist = glob.glob(os.path.join(cpdir, cpfileglob))

    return add_cmds_cplist(cplist,
                           cmdpkl,
                           require_cmd_magcolor=require_cmd_magcolor,
                           save_cmd_pngs=save_cmd_pngs)