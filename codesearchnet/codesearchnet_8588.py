def force_fresh_session(view):
    """
    View decorator which terminates stale TPA sessions.

    This decorator forces the user to obtain a new session
    the first time they access the decorated view. This prevents
    TPA-authenticated users from hijacking the session of another
    user who may have been previously logged in using the same
    browser window.

    This decorator should be used in conjunction with the
    enterprise_login_required decorator.

    Usage::
        @enterprise_login_required
        @force_fresh_session()
        def my_view(request, enterprise_uuid):
            # Some functionality ...

        OR

        class MyView(View):
            ...
            @method_decorator(enterprise_login_required)
            @method_decorator(force_fresh_session)
            def get(self, request, enterprise_uuid):
                # Some functionality ...
    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        """
        Wrap the function.
        """
        if not request.GET.get(FRESH_LOGIN_PARAMETER):
            # The enterprise_login_required decorator promises to set the fresh login URL
            # parameter for this URL when it was the agent that initiated the login process;
            # if that parameter isn't set, we can safely assume that the session is "stale";
            # that isn't necessarily an issue, though. Redirect the user to
            # log out and then come back here - the enterprise_login_required decorator will
            # then take effect prior to us arriving back here again.
            enterprise_customer = get_enterprise_customer_or_404(kwargs.get('enterprise_uuid'))
            provider_id = enterprise_customer.identity_provider or ''
            sso_provider = get_identity_provider(provider_id)
            if sso_provider:
                # Parse the current request full path, quote just the path portion,
                # then reconstruct the full path string.
                # The path and query portions should be the only non-empty strings here.
                scheme, netloc, path, params, query, fragment = urlparse(request.get_full_path())
                redirect_url = urlunparse((scheme, netloc, quote(path), params, query, fragment))

                return redirect(
                    '{logout_url}?{params}'.format(
                        logout_url='/logout',
                        params=urlencode(
                            {'redirect_url': redirect_url}
                        )
                    )
                )
        return view(request, *args, **kwargs)

    return wrapper