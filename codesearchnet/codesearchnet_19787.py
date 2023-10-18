def _dump_message(self, m, top=''):
        """Dump single message type.
        
        Keyword arguments:
        top -- top namespace
        """
        self._print()
        self._print('message {} {{'.format(m.name))
        self.defines.append('{}.{}'.format(top, m.name))
        self.tabs+=1
        
        for f in m.field:
            self._dump_field(f)
        
        for e in m.enum_type:
            self._dump_enum(e, top='{}.{}'.format(top, m.name))
        
        for n in m.nested_type:
            self._dump_message(n, top='{}.{}'.format(top, m.name))
        
        self.tabs-=1
        self._print('}')