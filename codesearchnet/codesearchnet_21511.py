def html_title(self):
        """HTML5-formatted document title (`str`)."""
        return self.format_title(format='html5', deparagraph=True,
                                 mathjax=False, smart=True)