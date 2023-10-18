def upsert_users(cursor, user_ids):
    """Given a set of user identifiers (``user_ids``),
    upsert them into the database after checking accounts for
    the latest information.
    """
    accounts = get_current_registry().getUtility(IOpenstaxAccounts)

    def lookup_profile(username):
        profile = accounts.get_profile_by_username(username)
        # See structure documentation at:
        #   https://<accounts-instance>/api/docs/v1/users/index
        if profile is None:
            raise UserFetchError(username)

        opt_attrs = ('first_name', 'last_name', 'full_name',
                     'title', 'suffix',)
        for attr in opt_attrs:
            profile.setdefault(attr, None)
        return profile

    _upsert_users(cursor, user_ids, lookup_profile)
    _upsert_persons(cursor, user_ids, lookup_profile)