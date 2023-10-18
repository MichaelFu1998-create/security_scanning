def collect_genv(self, include_local=True, include_global=True):
        """
        Returns a copy of the global environment with all the local variables copied back into it.
        """
        e = type(self.genv)()
        if include_global:
            e.update(self.genv)
        if include_local:
            for k, v in self.lenv.items():
                e['%s_%s' % (self.obj.name.lower(), k)] = v
        return e