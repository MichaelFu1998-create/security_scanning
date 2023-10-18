def _get_metadata(self):
        """ Get image metadata from filename.md: title, description, meta."""
        self.description = ''
        self.meta = {}
        self.title = ''

        descfile = splitext(self.src_path)[0] + '.md'
        if isfile(descfile):
            meta = read_markdown(descfile)
            for key, val in meta.items():
                setattr(self, key, val)