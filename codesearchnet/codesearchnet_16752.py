def get_dynamic_base(self, bases: tuple):
        """Create of get a base space for a tuple of bases"""

        try:
            return self._dynamic_bases_inverse[bases]
        except KeyError:
            name = self._dynamic_base_namer.get_next(self._dynamic_bases)
            base = self._new_space(name=name)
            self.spacegraph.add_space(base)
            self._dynamic_bases[name] = base
            self._dynamic_bases_inverse[bases] = base
            base.add_bases(bases)
            return base