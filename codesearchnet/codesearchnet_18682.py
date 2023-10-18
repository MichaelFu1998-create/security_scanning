def handle_starttag(self, tag, attrs):
        """Return representation of html start tag and attributes."""
        if tag in self.mathml_elements:
            final_attr = ""
            for key, value in attrs:
                final_attr += ' {0}="{1}"'.format(key, value)
            self.fed.append("<{0}{1}>".format(tag, final_attr))