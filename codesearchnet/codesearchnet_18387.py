def read_docs(self, docsfiles):
        """Read program documentation from a DocParser compatible file.

        docsfiles is a list of paths to potential docsfiles: parse if present.
        A string is taken as a list of one item.
        """
        updates = DocParser()
        for docsfile in _list(docsfiles):
            if os.path.isfile(docsfile):
                updates.parse(docsfile)
        self.docs.update((k, _docs(updates[k], self.docvars)) for k in self.docs if updates.blocks[k])
        for name, text in updates['parameters'].items():
            if name in self:
                self.getparam(name).docs = text[0] % self.docvars
            elif name not in self.ignore:
                raise ValueError("parameter %r does not exist" % name)