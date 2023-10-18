def _dump_field(self, fd):
        """Dump single field.
        """
        v = {}
        v['label'] = Pbd.LABELS[fd.label]
        v['type'] = fd.type_name if len(fd.type_name) > 0 else Pbd.TYPES[fd.type]
        v['name'] = fd.name
        v['number'] = fd.number
        v['default'] = '[default = {}]'.format(fd.default_value) if len(fd.default_value) > 0 else ''
        
        f = '{label} {type} {name} = {number} {default};'.format(**v)
        f = ' '.join(f.split())
        self._print(f)
        
        if len(fd.type_name) > 0:
            self.uses.append(fd.type_name)