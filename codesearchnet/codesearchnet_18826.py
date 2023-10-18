def get_collection(self, journal):
        """Return this articles' collection."""
        conference = ''
        for tag in self.document.getElementsByTagName('conference'):
            conference = xml_to_text(tag)
        if conference or journal == "International Journal of Modern Physics: Conference Series":
            return [('a', 'HEP'), ('a', 'ConferencePaper')]
        elif self._get_article_type() == "review-article":
            return [('a', 'HEP'), ('a', 'Review')]
        else:
            return [('a', 'HEP'), ('a', 'Published')]