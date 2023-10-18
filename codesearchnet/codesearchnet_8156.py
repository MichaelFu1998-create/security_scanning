def single(method):
    """Decorator for RestServer methods that take a single address"""
    @functools.wraps(method)
    def single(self, address, value=None):
        address = urllib.parse.unquote_plus(address)
        try:
            error = NO_PROJECT_ERROR
            if not self.project:
                raise ValueError
            error = BAD_ADDRESS_ERROR
            ed = editor.Editor(address, self.project)

            if value is None:
                error = BAD_GETTER_ERROR
                result = method(self, ed)
            else:
                error = BAD_SETTER_ERROR
                result = method(self, ed, value)
            result = {'value': result}

        except Exception as e:
            traceback.print_exc()
            msg = '%s\n%s' % (error.format(**locals()), e)
            result = {'error': msg}

        return flask.jsonify(result)

    return single