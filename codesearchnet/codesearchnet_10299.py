def get_volume(f):
    """Return the volume in nm^3 of structure file *f*.

    (Uses :func:`gromacs.editconf`; error handling is not good)
    """
    fd, temp = tempfile.mkstemp('.gro')
    try:
        rc,out,err = gromacs.editconf(f=f, o=temp, stdout=False)
    finally:
        os.unlink(temp)
    return [float(x.split()[1]) for x in out.splitlines()
            if x.startswith('Volume:')][0]