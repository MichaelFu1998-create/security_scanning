def _prep_snippet_for_pandoc(self, latex_text):
        """Process a LaTeX snippet of content for better transformation
        with pandoc.

        Currently runs the CitationLinker to convert BibTeX citations to
        href links.
        """
        replace_cite = CitationLinker(self.bib_db)
        latex_text = replace_cite(latex_text)
        return latex_text