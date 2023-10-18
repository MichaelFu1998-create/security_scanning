def format_abstract(self, format='html5', deparagraph=False, mathjax=False,
                        smart=True, extra_args=None):
        """Get the document abstract in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
        deparagraph : `bool`, optional
            Remove the paragraph tags from single paragraph content.
        mathjax : `bool`, optional
            Allow pandoc to use MathJax math markup.
        smart : `True`, optional
            Allow pandoc to create "smart" unicode punctuation.
        extra_args : `list`, optional
            Additional command line flags to pass to Pandoc. See
            `lsstprojectmeta.pandoc.convert.convert_text`.

        Returns
        -------
        output_text : `str`
            Converted content or `None` if the title is not available in
            the document.
        """
        if self.abstract is None:
            return None

        abstract_latex = self._prep_snippet_for_pandoc(self.abstract)

        output_text = convert_lsstdoc_tex(
            abstract_latex, format,
            deparagraph=deparagraph,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text