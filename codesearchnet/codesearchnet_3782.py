def request(self, method, url, *args, **kwargs):
        """Make a request to the Ansible Tower API, and return the
        response.
        """

        # If the URL has the api/vX at the front strip it off
        # This is common to have if you are extracting a URL from an existing object.
        # For example, any of the 'related' fields of an object will have this
        import re
        url = re.sub("^/?api/v[0-9]+/", "", url)

        # Piece together the full URL.
        use_version = not url.startswith('/o/')
        url = '%s%s' % (self.get_prefix(use_version), url.lstrip('/'))

        # Ansible Tower expects authenticated requests; add the authentication
        # from settings if it's provided.
        kwargs.setdefault(
            'auth',
            BasicTowerAuth(
                settings.username,
                settings.password,
                self
            )
        )

        # POST and PUT requests will send JSON by default; make this
        # the content_type by default.  This makes it such that we don't have
        # to constantly write that in our code, which gets repetitive.
        headers = kwargs.get('headers', {})
        if method.upper() in ('PATCH', 'POST', 'PUT'):
            headers.setdefault('Content-Type', 'application/json')
            kwargs['headers'] = headers

        # If debugging is on, print the URL and data being sent.
        debug.log('%s %s' % (method, url), fg='blue', bold=True)
        if method in ('POST', 'PUT', 'PATCH'):
            debug.log('Data: %s' % kwargs.get('data', {}),
                      fg='blue', bold=True)
        if method == 'GET' or kwargs.get('params', None):
            debug.log('Params: %s' % kwargs.get('params', {}),
                      fg='blue', bold=True)
        debug.log('')

        # If this is a JSON request, encode the data value.
        if headers.get('Content-Type', '') == 'application/json':
            kwargs['data'] = json.dumps(kwargs.get('data', {}))

        r = self._make_request(method, url, args, kwargs)

        # Sanity check: Did the server send back some kind of internal error?
        # If so, bubble this up.
        if r.status_code >= 500:
            raise exc.ServerError('The Tower server sent back a server error. '
                                  'Please try again later.')

        # Sanity check: Did we fail to authenticate properly?
        # If so, fail out now; this is always a failure.
        if r.status_code == 401:
            raise exc.AuthError('Invalid Tower authentication credentials (HTTP 401).')

        # Sanity check: Did we get a forbidden response, which means that
        # the user isn't allowed to do this? Report that.
        if r.status_code == 403:
            raise exc.Forbidden("You don't have permission to do that (HTTP 403).")

        # Sanity check: Did we get a 404 response?
        # Requests with primary keys will return a 404 if there is no response,
        # and we want to consistently trap these.
        if r.status_code == 404:
            raise exc.NotFound('The requested object could not be found.')

        # Sanity check: Did we get a 405 response?
        # A 405 means we used a method that isn't allowed. Usually this
        # is a bad request, but it requires special treatment because the
        # API sends it as a logic error in a few situations (e.g. trying to
        # cancel a job that isn't running).
        if r.status_code == 405:
            raise exc.MethodNotAllowed(
                "The Tower server says you can't make a request with the "
                "%s method to that URL (%s)." % (method, url),
            )

        # Sanity check: Did we get some other kind of error?
        # If so, write an appropriate error message.
        if r.status_code >= 400:
            raise exc.BadRequest(
                'The Tower server claims it was sent a bad request.\n\n'
                '%s %s\nParams: %s\nData: %s\n\nResponse: %s' %
                (method, url, kwargs.get('params', None),
                 kwargs.get('data', None), r.content.decode('utf8'))
            )

        # Django REST Framework intelligently prints API keys in the
        # order that they are defined in the models and serializer.
        #
        # We want to preserve this behavior when it is possible to do so
        # with minimal effort, because while the order has no explicit meaning,
        # we make some effort to order keys in a convenient manner.
        #
        # To this end, make this response into an APIResponse subclass
        # (defined below), which has a `json` method that doesn't lose key
        # order.
        r.__class__ = APIResponse

        # Return the response object.
        return r