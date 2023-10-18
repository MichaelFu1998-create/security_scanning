def _arg_name(self, name, types, prefix="--"):
        if 'type:a10_nullable' in types:
            return self._arg_name(name, types['type:a10_nullable'], prefix)

        if 'type:a10_list' in types:
            return self._arg_name(name, types['type:a10_list'], prefix)

        if 'type:a10_reference' in types:
            if name.endswith('_id'):
                name = name[:-3]

        """--shish-kabob it"""
        return prefix + name.replace('_', '-')