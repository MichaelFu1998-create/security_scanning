def _dump_enum(self, e, top=''):
        """Dump single enum type.
        
        Keyword arguments:
        top -- top namespace
        """
        self._print()
        self._print('enum {} {{'.format(e.name))
        self.defines.append('{}.{}'.format(top,e.name))
        
        self.tabs+=1
        for v in e.value:
            self._print('{} = {};'.format(v.name, v.number))
        self.tabs-=1
        self._print('}')