def put(self, key, value, attrs=None, format=None, append=False, **kwargs):
        """
        Store object in HDFStore

        Parameters
        ----------
        key : str

        value : {Series, DataFrame, Panel, Numpy ndarray}

        format : 'fixed(f)|table(t)', default is 'fixed'
            fixed(f) : Fixed format
                Fast writing/reading. Not-appendable, nor searchable

            table(t) : Table format
                Write as a PyTables Table structure which may perform worse but allow more flexible operations
                like searching/selecting subsets of the data

        append : boolean, default False
            This will force Table format, append the input data to the
            existing.

        encoding : default None, provide an encoding for strings
        """
        if not isinstance(value, np.ndarray):
            super(NumpyHDFStore, self).put(key, value, format, append, **kwargs)
        else:
            group = self.get_node(key)

            # remove the node if we are not appending
            if group is not None and not append:
                self._handle.removeNode(group, recursive=True)
                group = None

            if group is None:
                paths = key.split('/')

                # recursively create the groups
                path = '/'
                for p in paths:
                    if not len(p):
                        continue
                    new_path = path
                    if not path.endswith('/'):
                        new_path += '/'
                    new_path += p
                    group = self.get_node(new_path)
                    if group is None:
                        group = self._handle.createGroup(path, p)
                    path = new_path

            ds_name = kwargs.get('ds_name', self._array_dsname)

            ds = self._handle.createArray(group, ds_name, value)
            if attrs is not None:
                for key in attrs:
                    setattr(ds.attrs, key, attrs[key])

            self._handle.flush()

            return ds