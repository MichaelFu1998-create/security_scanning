def authorize_view(self):
        """Flask view that starts the authorization flow.

        Starts flow by redirecting the user to the OAuth2 provider.
        """
        args = request.args.to_dict()

        # Scopes will be passed as mutliple args, and to_dict() will only
        # return one. So, we use getlist() to get all of the scopes.
        args['scopes'] = request.args.getlist('scopes')

        return_url = args.pop('return_url', None)
        if return_url is None:
            return_url = request.referrer or '/'

        flow = self._make_flow(return_url=return_url, **args)
        auth_url = flow.step1_get_authorize_url()

        return redirect(auth_url)