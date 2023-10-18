def check_oauth2_scope(can_method, *myscopes):
    """Base permission factory that check OAuth2 scope and can_method.

    :param can_method: Permission check function that accept a record in input
        and return a boolean.
    :param myscopes: List of scopes required to permit the access.
    :returns: A :class:`flask_principal.Permission` factory.
    """
    def check(record, *args, **kwargs):
        @require_api_auth()
        @require_oauth_scopes(*myscopes)
        def can(self):
            return can_method(record)

        return type('CheckOAuth2Scope', (), {'can': can})()
    return check