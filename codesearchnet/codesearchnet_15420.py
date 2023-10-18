def _insert_optional_roles(cursor, model, ident):
    """Inserts the optional roles if values for the optional roles
    exist.
    """
    optional_roles = [
        # (<metadata-attr>, <db-role-id>,),
        ('translators', 4,),
        ('editors', 5,),
    ]
    for attr, role_id in optional_roles:
        roles = model.metadata.get(attr)
        if not roles:
            # Bail out, no roles for this type.
            continue
        usernames = [parse_user_uri(x['id']) for x in roles]
        cursor.execute("""\
INSERT INTO moduleoptionalroles (module_ident, roleid, personids)
VALUES (%s, %s, %s)""", (ident, role_id, usernames,))