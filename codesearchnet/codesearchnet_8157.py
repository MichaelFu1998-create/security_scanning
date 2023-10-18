def multi(method):
    """Decorator for RestServer methods that take multiple addresses"""
    @functools.wraps(method)
    def multi(self, address=''):
        values = flask.request.values
        address = urllib.parse.unquote_plus(address)
        if address and values and not address.endswith('.'):
            address += '.'

        result = {}
        for a in values or '':
            try:
                if not self.project:
                    raise ValueError('No Project is currently loaded')

                ed = editor.Editor(address + a, self.project)
                result[address + a] = {'value': method(self, ed, a)}
            except:
                if self.project:
                    traceback.print_exc()
                result[address + a] = {'error': 'Could not multi addr %s' % a}

        return flask.jsonify(result)

    return multi