def get(self, path):
        ''' return a configuration value

            usage:
                get('section.property')

            Note that currently array indexes are not supported. You must
            get the whole array.

            returns None if any path element or the property is missing
        '''
        path = _splitPath(path)
        for config in self.configs.values():
            cur = config
            for el in path:
                if el in cur:
                    cur = cur[el]
                else:
                    cur = None
                    break
            if cur is not None:
                return cur
        return None