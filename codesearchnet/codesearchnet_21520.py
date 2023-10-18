def format_authors(self, format='html5', deparagraph=True, mathjax=False,
                       smart=True, extra_args=None):
        """Get the document authors in the specified markup format.

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
        output_text : `list` of `str`
            Sequence of author names in the specified output markup format.
        """
        formatted_authors = []
        for latex_author in self.authors:
            formatted_author = convert_lsstdoc_tex(
                latex_author, format,
                deparagraph=deparagraph,
                mathjax=mathjax,
                smart=smart,
                extra_args=extra_args)
            # removes Pandoc's terminal newlines
            formatted_author = formatted_author.strip()
            formatted_authors.append(formatted_author)
        return formatted_authors