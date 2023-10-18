def set(self, path, value=None, filename=None):
        ''' Set a configuration value. If no filename is specified, the
            property is set in the first configuration file. Note that if a
            filename is specified and the property path is present in an
            earlier filename then set property will be hidden.

            usage:
                set('section.property', value='somevalue')

            Note that currently array indexes are not supported. You must
            set the whole array.
        '''
        if filename is None:
            config = self._firstConfig()[1]
        else:
            config = self.configs[filename]

        path = _splitPath(path)
        for el in path[:-1]:
            if el in config:
                config = config[el]
            else:
                config[el] = OrderedDict()
                config = config[el]
        config[path[-1]] = value