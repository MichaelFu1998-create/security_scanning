def _info(self, source, key, filetype, ignore):
        """
        Generates the union of the source.specs and the metadata
        dictionary loaded by the filetype object.
        """
        specs, mdata = [], {}
        mdata_clashes  = set()

        for spec in source.specs:
            if key not in spec:
                raise Exception("Key %r not available in 'source'." % key)

            mdata = dict((k,v) for (k,v) in filetype.metadata(spec[key]).items()
                         if k not in ignore)
            mdata_spec = {}
            mdata_spec.update(spec)
            mdata_spec.update(mdata)
            specs.append(mdata_spec)
            mdata_clashes = mdata_clashes | (set(spec.keys()) & set(mdata.keys()))
        # Metadata clashes can be avoided by using the ignore list.
        if mdata_clashes:
            self.warning("Loaded metadata keys overriding source keys.")
        return specs