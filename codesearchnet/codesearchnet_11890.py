def get_locale_dict(self, text=None):
        """
        Reads /etc/default/locale and returns a dictionary representing its key pairs.
        """
        text = text or self.cat_locale()
        # Format NAME="value".
        return dict(re.findall(r'^([a-zA-Z_]+)\s*=\s*[\'\"]*([0-8a-zA-Z_\.\:\-]+)[\'\"]*', text, re.MULTILINE))