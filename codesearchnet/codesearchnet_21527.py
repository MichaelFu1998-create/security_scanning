def _load_bib_db(self):
        r"""Load the BibTeX bibliography referenced by the document.

        This method triggered by the `bib_db` attribute and populates the
        `_bib_db` private attribute.

        The ``\bibliography`` command is parsed to identify the bibliographies
        referenced by the document.
        """
        # Get the names of custom bibtex files by parsing the
        # \bibliography command and filtering out the default lsstdoc
        # bibliographies.
        command = LatexCommand(
            'bibliography',
            {'name': 'bib_names', 'required': True, 'bracket': '{'})
        try:
            parsed = next(command.parse(self._tex))
            bib_names = [n.strip() for n in parsed['bib_names'].split(',')]
        except StopIteration:
            self._logger.warning('lsstdoc has no bibliography command')
            bib_names = []
        custom_bib_names = [n for n in bib_names
                            if n not in KNOWN_LSSTTEXMF_BIB_NAMES]

        # Read custom bibliographies.
        custom_bibs = []
        for custom_bib_name in custom_bib_names:
            custom_bib_path = os.path.join(
                os.path.join(self._root_dir),
                custom_bib_name + '.bib'
            )
            if not os.path.exists(custom_bib_path):
                self._logger.warning('Could not find bibliography %r',
                                     custom_bib_path)
                continue
            with open(custom_bib_path, 'r') as file_handle:
                custom_bibs.append(file_handle.read())
        if len(custom_bibs) > 0:
            custom_bibtex = '\n\n'.join(custom_bibs)
        else:
            custom_bibtex = None

        # Get the combined pybtex bibliography
        db = get_bibliography(bibtex=custom_bibtex)

        self._bib_db = db