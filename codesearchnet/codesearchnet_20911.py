def get_environ(self):
        """https://www.python.org/dev/peps/pep-0333/#environ-variables"""
        env = self.base_environ.copy()
        env['REQUEST_METHOD'] = self.request_method

        if '?' in self.path:
            path, query = self.path.split('?', 1)
        else:
            path, query = self.path, ''
        env['PATH_INFO'] = urllib.parse.unquote(path)
        env['QUERY_STRING'] = query

        env['CONTENT_TYPE'] = self.headers.get('Content-Type', '')
        env['CONTENT_LENGTH'] = self.headers.get('Content-Length', '0')

        env['SERVER_PROTOCOL'] = self.request_version
        env['REMOTE_ADDR'] = self.client_address[0]
        env['REMOTE_PORT'] = self.client_address[1]

        env['wsgi.version'] = (1, 0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.BytesIO(self.raw_request)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = True
        env['wsgi.run_once'] = False

        for k, v in self.headers.items():
            k = k.replace('-', '_').upper()
            if k in env:
                continue
            env['HTTP_' + k] = v
        return env