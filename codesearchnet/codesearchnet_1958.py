def _munge_whitespace(self, text):
        """_munge_whitespace(text : string) -> string

        Munge whitespace in text: expand tabs and convert all other
        whitespace characters to spaces.  Eg. " foo\\tbar\\n\\nbaz"
        becomes " foo    bar  baz".
        """
        if self.expand_tabs:
            # text = text.expandtabs()
            text = ' '.join((' '.join(text.split('\n'))).split('\t'))
        if self.replace_whitespace:
            # if isinstance(text, str):
            #     text = text.translate(self.whitespace_trans)
            # elif isinstance(text, _unicode):
            #     text = text.translate(self.unicode_whitespace_trans)
            text = ' '.join(' '.join(text.split('\n')).split('\t'))
        return text