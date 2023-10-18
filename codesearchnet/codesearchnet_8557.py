def course_discovery_api_client(user, catalog_url):
    """
    Return a Course Discovery API client setup with authentication for the specified user.
    """
    if JwtBuilder is None:
        raise NotConnectedToOpenEdX(
            _("To get a Catalog API client, this package must be "
              "installed in an Open edX environment.")
        )

    jwt = JwtBuilder.create_jwt_for_user(user)
    return EdxRestApiClient(catalog_url, jwt=jwt)