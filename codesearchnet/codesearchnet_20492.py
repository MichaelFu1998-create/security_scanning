def ux_file_len(filepath):
    """Returns the length of the file using the 'wc' GNU command

    Parameters
    ----------
    filepath: str

    Returns
    -------
    float
    """
    p = subprocess.Popen(['wc', '-l', filepath], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()

    if p.returncode != 0:
        raise IOError(err)

    l = result.strip()
    l = int(l.split()[0])
    return l