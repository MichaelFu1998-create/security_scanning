def _activate(self):
        '''
        Do some serious mangling to the current python environment...
        This is necessary to activate an environment via python.
        '''

        old_syspath = set(sys.path)
        site.addsitedir(self.site_path)
        site.addsitedir(self.bin_path)
        new_syspaths = set(sys.path) - old_syspath
        for path in new_syspaths:
            sys.path.remove(path)
            sys.path.insert(1, path)

        if not hasattr(sys, 'real_prefix'):
            sys.real_prefix = sys.prefix

        sys.prefix = self.path