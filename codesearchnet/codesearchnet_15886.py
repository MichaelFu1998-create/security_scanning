def _get_doc(self, name):
        """
        Get the documentation of an Octave procedure or object.

        Parameters
        ----------
        name : str
            Function name to search for.

        Returns
        -------
        out : str
          Documentation string.

        Raises
        ------
        Oct2PyError
           If the procedure or object function has a syntax error.

        """
        doc = 'No documentation for %s' % name

        engine = self._engine

        doc = engine.eval('help("%s")' % name, silent=True)

        if 'syntax error:' in doc.lower():
            raise Oct2PyError(doc)

        if 'error:' in doc.lower():
            doc = engine.eval('type("%s")' % name, silent=True)
            doc = '\n'.join(doc.splitlines()[:3])

        default = self.feval.__doc__
        default = '        ' + default[default.find('func_args:'):]
        default = '\n'.join([line[8:] for line in default.splitlines()])

        doc = '\n'.join(doc.splitlines())
        doc = '\n' + doc + '\n\nParameters\n----------\n' + default
        doc += '\n**kwargs - Deprecated keyword arguments\n\n'
        doc += 'Notes\n-----\n'
        doc += 'Keyword arguments to dynamic functions are deprecated.\n'
        doc += 'The `plot_*` kwargs will be ignored, but the rest will\n'
        doc += 'used as key - value pairs as in version 3.x.\n'
        doc += 'Use `set_plot_settings()` for plot settings, and use\n'
        doc += '`func_args` directly for key - value pairs.'
        return doc