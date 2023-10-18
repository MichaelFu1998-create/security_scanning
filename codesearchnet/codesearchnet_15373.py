def _dissect_roles(metadata):
    """Given a model's ``metadata``, iterate over the roles.
    Return values are the role identifier and role type as a tuple.
    """
    for role_key in cnxepub.ATTRIBUTED_ROLE_KEYS:
        for user in metadata.get(role_key, []):
            if user['type'] != 'cnx-id':
                raise ValueError("Archive only accepts Connexions users.")
            uid = parse_user_uri(user['id'])
            yield uid, role_key
    raise StopIteration()