def html_short_title(self):
        """HTML5-formatted document short title (`str`)."""
        return self.format_short_title(format='html5', deparagraph=True,
                                       mathjax=False, smart=True)