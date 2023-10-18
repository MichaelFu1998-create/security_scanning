def _parse_error(self, err):
        """Create a traceback for an Octave evaluation error.
        """
        self.logger.debug(err)
        stack = err.get('stack', [])
        if not err['message'].startswith('parse error:'):
            err['message'] = 'error: ' + err['message']
        errmsg = 'Octave evaluation error:\n%s' % err['message']

        if not isinstance(stack, StructArray):
            return errmsg

        errmsg += '\nerror: called from:'
        for item in stack[:-1]:
            errmsg += '\n    %(name)s at line %(line)d' % item
            try:
                errmsg += ', column %(column)d' % item
            except Exception:
                pass
        return errmsg