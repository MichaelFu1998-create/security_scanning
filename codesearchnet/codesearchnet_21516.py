def format_content(self, format='plain', mathjax=False,
                       smart=True, extra_args=None):
        """Get the document content in the specified markup format.

        Parameters
        ----------
        format : `str`, optional
            Output format (such as ``'html5'`` or ``'plain'``).
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
            Converted content.
        """
        output_text = convert_lsstdoc_tex(
            self._tex, format,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text