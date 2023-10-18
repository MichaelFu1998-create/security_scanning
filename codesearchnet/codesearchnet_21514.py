def html_abstract(self):
        """HTML5-formatted document abstract (`str`)."""
        return self.format_abstract(format='html5', deparagraph=False,
                                    mathjax=False, smart=True)