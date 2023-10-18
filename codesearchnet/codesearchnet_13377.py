def _make_urp_hash(username, realm, passwd):
    """Compute MD5 sum of username:realm:password.

    :Parameters:
        - `username`: a username.
        - `realm`: a realm.
        - `passwd`: a password.
    :Types:
        - `username`: `bytes`
        - `realm`: `bytes`
        - `passwd`: `bytes`

    :return: the MD5 sum of the parameters joined with ':'.
    :returntype: `bytes`"""
    if realm is None:
        realm = b""
    return _h_value(b":".join((username, realm, passwd)))