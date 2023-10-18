def process_inputs(tex_source, root_dir=None):
    r"""Insert referenced TeX file contents (from  ``\input`` and ``\include``
    commands) into the source.

    Parameters
    ----------
    tex_source : `str`
        TeX source where referenced source files will be found and inserted.
    root_dir : `str`, optional
        Name of the directory containing the TeX project's root file. Files
        referenced by TeX ``\input`` and ``\include`` commands are relative to
        this directory. If not set, the current working directory is assumed.

    Returns
    -------
    tex_source : `str`
        TeX source.

    See also
    --------
    `read_tex_file`
        Recommended API for reading a root TeX source file and inserting
        referenced files.
    """
    logger = logging.getLogger(__name__)

    def _sub_line(match):
        """Function to be used with re.sub to inline files for each match."""
        fname = match.group('filename')
        if not fname.endswith('.tex'):
            full_fname = ".".join((fname, 'tex'))
        else:
            full_fname = fname
        full_path = os.path.abspath(os.path.join(root_dir, full_fname))

        try:
            included_source = read_tex_file(full_path, root_dir=root_dir)
        except IOError:
            logger.error("Cannot open {0} for inclusion".format(full_path))
            raise
        else:
            return included_source

    tex_source = input_include_pattern.sub(_sub_line, tex_source)
    return tex_source