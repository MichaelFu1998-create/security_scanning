def freeze(self):
        """Create a usable data structure for serializing."""
        data = super(IndexBuilder, self).freeze()
        try:
            # Sphinx >= 1.5 format
            # Due to changes from github.com/sphinx-doc/sphinx/pull/2454
            base_file_names = data['docnames']
        except KeyError:
            # Sphinx < 1.5 format
            base_file_names = data['filenames']

        store = {}
        c = itertools.count()
        for prefix, items in iteritems(data['objects']):
            for name, (index, typeindex, _, shortanchor) in iteritems(items):
                objtype = data['objtypes'][typeindex]
                if objtype.startswith('cpp:'):
                    split =  name.rsplit('::', 1)
                    if len(split) != 2:
                        warnings.warn("What's up with %s?" % str((prefix, name, objtype)))
                        continue
                    prefix, name = split
                    last_prefix = prefix.split('::')[-1]
                else:
                    last_prefix = prefix.split('.')[-1]

                store[next(c)] = {
                    'filename': base_file_names[index],
                    'objtype': objtype,
                    'prefix': prefix,
                    'last_prefix': last_prefix,
                    'name': name,
                    'shortanchor': shortanchor,
                }

        data.update({'store': store})
        return data