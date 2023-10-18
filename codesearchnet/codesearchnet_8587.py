def enterprise_login_required(view):
    """
    View decorator for allowing authenticated user with valid enterprise UUID.

    This decorator requires enterprise identifier as a parameter
    `enterprise_uuid`.

    This decorator will throw 404 if no kwarg `enterprise_uuid` is provided to
    the decorated view .

    If there is no enterprise in database against the kwarg `enterprise_uuid`
    or if the user is not authenticated then it will redirect the user to the
    enterprise-linked SSO login page.

    Usage::
        @enterprise_login_required()
        def my_view(request, enterprise_uuid):
            # Some functionality ...

        OR

        class MyView(View):
            ...
            @method_decorator(enterprise_login_required)
            def get(self, request, enterprise_uuid):
                # Some functionality ...

    """
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        """
        Wrap the decorator.
        """
        if 'enterprise_uuid' not in kwargs:
            raise Http404

        enterprise_uuid = kwargs['enterprise_uuid']
        enterprise_customer = get_enterprise_customer_or_404(enterprise_uuid)

        # Now verify if the user is logged in. If user is not logged in then
        # send the user to the login screen to sign in with an
        # Enterprise-linked IdP and the pipeline will get them back here.
        if not request.user.is_authenticated:
            parsed_current_url = urlparse(request.get_full_path())
            parsed_query_string = parse_qs(parsed_current_url.query)
            parsed_query_string.update({
                'tpa_hint': enterprise_customer.identity_provider,
                FRESH_LOGIN_PARAMETER: 'yes'
            })
            next_url = '{current_path}?{query_string}'.format(
                current_path=quote(parsed_current_url.path),
                query_string=urlencode(parsed_query_string, doseq=True)
            )
            return redirect(
                '{login_url}?{params}'.format(
                    login_url='/login',
                    params=urlencode(
                        {'next': next_url}
                    )
                )
            )

        # Otherwise, they can proceed to the original view.
        return view(request, *args, **kwargs)

    return wrapper