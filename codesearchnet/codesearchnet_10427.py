def get_lipid_vdwradii(outdir=os.path.curdir, libdir=None):
    """Find vdwradii.dat and add special entries for lipids.

    See :data:`gromacs.setup.vdw_lipid_resnames` for lipid
    resnames. Add more if necessary.
    """
    vdwradii_dat = os.path.join(outdir, "vdwradii.dat")

    if libdir is not None:
        filename = os.path.join(libdir, 'vdwradii.dat')  # canonical name
        if not os.path.exists(filename):
            msg = 'No VDW database file found in {filename!r}.'.format(**vars())
            logger.exception(msg)
            raise OSError(msg, errno.ENOENT)
    else:
        try:
            filename = os.path.join(os.environ['GMXLIB'], 'vdwradii.dat')
        except KeyError:
            try:
                filename = os.path.join(os.environ['GMXDATA'], 'top', 'vdwradii.dat')
            except KeyError:
                msg = "Cannot find vdwradii.dat. Set GMXLIB (point to 'top') or GMXDATA ('share/gromacs')."
                logger.exception(msg)
                raise OSError(msg, errno.ENOENT)
    if not os.path.exists(filename):
        msg = "Cannot find {filename!r}; something is wrong with the Gromacs installation.".format(**vars())
        logger.exception(msg, errno.ENOENT)
        raise OSError(msg)

    # make sure to catch 3 and 4 letter resnames
    patterns = vdw_lipid_resnames + list({x[:3] for x in vdw_lipid_resnames})
    # TODO: should do a tempfile...
    with open(vdwradii_dat, 'w') as outfile:
        # write lipid stuff before general
        outfile.write('; Special larger vdw radii for solvating lipid membranes\n')
        for resname in patterns:
            for atom,radius in vdw_lipid_atom_radii.items():
                outfile.write('{resname:4!s} {atom:<5!s} {radius:5.3f}\n'.format(**vars()))
        with open(filename, 'r') as infile:
            for line in infile:
                outfile.write(line)
    logger.debug('Created lipid vdW radii file {vdwradii_dat!r}.'.format(**vars()))
    return realpath(vdwradii_dat)