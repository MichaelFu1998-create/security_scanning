def add_cmds_cplist(cplist, cmdpkl,
                    require_cmd_magcolor=True,
                    save_cmd_pngs=False):
    '''This adds CMDs for each object in cplist.

    Parameters
    ----------

    cplist : list of str
        This is the input list of checkplot pickles to add the CMDs to.

    cmdpkl : str
        This is the filename of the CMD pickle created previously.

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

    # load the CMD first to save on IO
    with open(cmdpkl,'rb') as infd:
        cmd = pickle.load(infd)

    for cpf in cplist:

        add_cmd_to_checkplot(cpf, cmd,
                             require_cmd_magcolor=require_cmd_magcolor,
                             save_cmd_pngs=save_cmd_pngs)