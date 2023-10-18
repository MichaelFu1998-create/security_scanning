def json_rpc_format(self):
        """Return the Exception data in a format for JSON-RPC
        """

        error = {
            'name': text_type(self.__class__.__name__),
            'code': self.code,
            'message': '{0}'.format(text_type(self.message)),
            'data': self.data
        }

        if current_app.config['DEBUG']:
            import sys, traceback
            error['stack'] = traceback.format_exc()
            error['executable'] = sys.executable

        return error