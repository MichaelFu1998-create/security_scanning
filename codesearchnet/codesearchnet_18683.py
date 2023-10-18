def handle_endtag(self, tag):
        """Return representation of html end tag."""
        if tag in self.mathml_elements:
            self.fed.append("</{0}>".format(tag))