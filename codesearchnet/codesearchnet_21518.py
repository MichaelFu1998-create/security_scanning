def format_short_title(self, format='html5', deparagraph=True,
                           mathjax=False, smart=True, extra_args=None):
        """Get the document short title in the specified markup format.

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
            Converted content or `None` if the short title is not available in
            the document.
        """
        if self.short_title is None:
            return None

        output_text = convert_lsstdoc_tex(
            self.short_title, 'html5',
            deparagraph=deparagraph,
            mathjax=mathjax,
            smart=smart,
            extra_args=extra_args)
        return output_text