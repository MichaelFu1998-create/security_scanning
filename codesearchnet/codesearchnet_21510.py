def read(cls, root_tex_path):
        """Construct an `LsstLatexDoc` instance by reading and parsing the
        LaTeX source.

        Parameters
        ----------
        root_tex_path : `str`
            Path to the LaTeX source on the filesystem. For multi-file LaTeX
            projects this should be the path to the root document.

        Notes
        -----
        This method implements the following pipeline:

        1. `lsstprojectmeta.tex.normalizer.read_tex_file`
        2. `lsstprojectmeta.tex.scraper.get_macros`
        3. `lsstprojectmeta.tex.normalizer.replace_macros`

        Thus ``input`` and ``includes`` are resolved along with simple macros.
        """
        # Read and normalize the TeX source, replacing macros with content
        root_dir = os.path.dirname(root_tex_path)
        tex_source = read_tex_file(root_tex_path)
        tex_macros = get_macros(tex_source)
        tex_source = replace_macros(tex_source, tex_macros)
        return cls(tex_source, root_dir=root_dir)