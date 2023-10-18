def html_authors(self):
        """HTML5-formatted authors (`list` of `str`)."""
        return self.format_authors(format='html5', deparagraph=True,
                                   mathjax=False, smart=True)