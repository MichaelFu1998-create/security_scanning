def _set_options(self, options):
        '''Private function for setting options used for sealing'''
        if not options:
            return self.options.copy()

        options = options.copy()

        if 'magic' in options:
            self.set_magic(options['magic'])
            del(options['magic'])

        if 'flags' in options:
            flags = options['flags']
            del(options['flags'])
            for key, value in flags.iteritems():
                if not isinstance(value, bool):
                    raise TypeError('Invalid flag type for: %s' % key)
        else:
            flags = self.options['flags']

        if 'info' in options:
            del(options['info'])

        for key, value in options.iteritems():
            if not isinstance(value, int):
                raise TypeError('Invalid option type for: %s' % key)
            if value < 0 or value > 255:
                raise ValueError('Option value out of range for: %s' % key)

        new_options = self.options.copy()
        new_options.update(options)
        new_options['flags'].update(flags)

        return new_options