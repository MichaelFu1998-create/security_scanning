def read_tex_file(root_filepath, root_dir=None):
    r"""Read a TeX file, automatically processing and normalizing it
    (including other input files, removing comments, and deleting trailing
    whitespace).

    Parameters
    ----------
    root_filepath : `str`
        Filepath to a TeX file.
    root_dir : `str`
        Root directory of the TeX project. This only needs to be set when
        recursively reading in ``\input`` or ``\include`` files.

    Returns
    -------
    tex_source : `str`
        TeX source.
    """
    with open(root_filepath, 'r') as f:
        tex_source = f.read()

    if root_dir is None:
        root_dir = os.path.dirname(root_filepath)

    # Text processing pipline
    tex_source = remove_comments(tex_source)
    tex_source = remove_trailing_whitespace(tex_source)
    tex_source = process_inputs(tex_source, root_dir=root_dir)

    return tex_source