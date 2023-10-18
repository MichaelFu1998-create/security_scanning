def _validate_roles(model):
    """Given the model, check that all the metadata role values
    have valid information in them and any required metadata fields
    contain values.
    """
    required_roles = (ATTRIBUTED_ROLE_KEYS[0], ATTRIBUTED_ROLE_KEYS[4],)
    for role_key in ATTRIBUTED_ROLE_KEYS:
        try:
            roles = model.metadata[role_key]
        except KeyError:
            if role_key in required_roles:
                raise exceptions.MissingRequiredMetadata(role_key)
        else:
            if role_key in required_roles and len(roles) == 0:
                raise exceptions.MissingRequiredMetadata(role_key)
        for role in roles:
            if role.get('type') != 'cnx-id':
                raise exceptions.InvalidRole(role_key, role)