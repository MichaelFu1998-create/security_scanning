def trj_fitandcenter(xy=False, **kwargs):
    """Center everything and make a compact representation (pass 1) and fit the system to a reference (pass 2).

    :Keywords:
       *s*
           input structure file (tpr file required to make molecule whole);
           if a list or tuple is provided then s[0] is used for pass 1 (should be a tpr)
           and s[1] is used for the fitting step (can be a pdb of the whole system)

           If a second structure is supplied then it is assumed that the fitted
           trajectory should *not* be centered.
       *f*
           input trajectory
       *o*
           output trajectory
       *input*
           A list with three groups. The default is
               ['backbone', 'protein','system']
           The fit command uses all three (1st for least square fit,
           2nd for centering, 3rd for output), the centered/make-whole stage use
           2nd for centering and 3rd for output.
       *input1*
           If *input1* is supplied then *input* is used exclusively
           for the fitting stage (pass 2) and *input1* for the centering (pass 1).
       *n*
           Index file used for pass 1 and pass 2.
       *n1*
           If *n1* is supplied then index *n1* is only used for pass 1
           (centering) and *n* for pass 2 (fitting).
       *xy* : boolean
           If ``True`` then only do a rot+trans fit in the xy plane
           (good for membrane simulations); default is ``False``.
       *kwargs*
           All other arguments are passed to :class:`~gromacs.tools.Trjconv`.

    Note that here we first center the protein and create a compact box, using
    ``-pbc mol -ur compact -center -boxcenter tric`` and write an intermediate
    xtc. Then in a second pass we perform a rotation+translation fit (or
    restricted to the xy plane if *xy* = ``True`` is set) on the intermediate
    xtc to produce the final trajectory. Doing it in this order has the
    disadvantage that the solvent box is rotating around the protein but the
    opposite order (with center/compact second) produces strange artifacts
    where columns of solvent appear cut out from the box---it probably means
    that after rotation the information for the periodic boundaries is not
    correct any more.

    Most kwargs are passed to both invocations of
    :class:`gromacs.tools.Trjconv` so it does not really make sense to use eg
    *skip*; in this case do things manually.

    By default the *input* to the fit command is ('backbone',
    'protein','system'); the compact command always uses the second and third
    group for its purposes or if this fails, prompts the user.

    Both steps cannot performed in one pass; this is a known limitation of
    ``trjconv``. An intermediate temporary XTC files is generated which should
    be automatically cleaned up unless bad things happened.

    The function tries to honour the input/output formats. For instance, if you
    want trr output you need to supply a trr file as input and explicitly give
    the output file also a trr suffix.

    .. Note:: For big trajectories it can **take a very long time**
              and consume a **large amount of temporary diskspace**.

    We follow the `g_spatial documentation`_ in preparing the trajectories::

       trjconv -s a.tpr -f a.xtc -o b.xtc -center -boxcenter tric -ur compact -pbc mol
       trjconv -s a.tpr -f b.xtc -o c.xtc -fit rot+trans

    .. _`g_spatial documentation`: http://www.gromacs.org/Documentation/Gromacs_Utilities/g_spatial
    """
    if xy:
        fitmode = 'rotxy+transxy'
        kwargs.pop('fit', None)
    else:
        fitmode = kwargs.pop('fit', 'rot+trans')  # user can use progressive, too

    intrj = kwargs.pop('f', None)
    # get the correct suffix for the intermediate step: only trr will
    # keep velocities/forces!
    suffix = os.path.splitext(intrj)[1]
    if not suffix in ('xtc', 'trr'):
        suffix = '.xtc'
    outtrj = kwargs.pop('o', None)

    ndx = kwargs.pop('n', None)
    ndxcompact = kwargs.pop('n1', ndx)

    structures = kwargs.pop('s', None)
    if type(structures) in (tuple, list):
        try:
            compact_structure, fit_structure = structures
        except:
            raise ValueError("argument s must be a pair of tpr/pdb files or a single structure file")
    else:
        compact_structure = fit_structure = structures


    inpfit = kwargs.pop('input', ('backbone', 'protein','system'))
    try:
        _inpcompact = inpfit[1:]     # use 2nd and 3rd group for compact
    except TypeError:
        _inpcompact = None
    inpcompact = kwargs.pop('input1', _inpcompact)  # ... or the user supplied ones

    fd, tmptrj = tempfile.mkstemp(suffix=suffix, prefix='pbc_compact_')

    logger.info("Input structure for PBC:  {compact_structure!r}".format(**vars()))
    logger.info("Input structure for fit:  {fit_structure!r}".format(**vars()))
    logger.info("Input trajectory:  {intrj!r}".format(**vars()))
    logger.info("Output trajectory: {outtrj!r}".format(**vars()))
    logger.debug("Writing temporary trajectory {tmptrj!r} (will be auto-cleaned).".format(**vars()))
    sys.stdout.flush()
    try:
        gromacs.trjconv(s=compact_structure, f=intrj, o=tmptrj, n=ndxcompact,
                        ur='compact', center=True, boxcenter='tric', pbc='mol',
                        input=inpcompact, **kwargs)
        # explicitly set pbc="none" for the fitting stage (anything else will produce rubbish and/or
        # complaints from Gromacs)
        kwargs['pbc'] = "none"
        if compact_structure == fit_structure:
            # fit as ususal, including centering
            # (Is center=True really necessary? -- note, if I remove center=True then
            # I MUST fiddle inpfit as below!!)
            gromacs.trjconv(s=fit_structure, f=tmptrj, o=outtrj, n=ndx, fit=fitmode, center=True, input=inpfit, **kwargs)
        else:
            # make sure that we fit EXACTLY as the user wants
            inpfit = [inpfit[0], inpfit[-1]]
            gromacs.trjconv(s=fit_structure, f=tmptrj, o=outtrj, n=ndx, fit=fitmode, input=inpfit, **kwargs)
    finally:
        utilities.unlink_gmx(tmptrj)