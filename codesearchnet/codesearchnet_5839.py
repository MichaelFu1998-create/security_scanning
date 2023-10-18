def get_subscriber_hash(member_email):
    """
    The MD5 hash of the lowercase version of the list member's email.
    Used as subscriber_hash

    :param member_email: The member's email address
    :type member_email: :py:class:`str`
    :returns: The MD5 hash in hex
    :rtype: :py:class:`str`
    """
    check_email(member_email)
    member_email = member_email.lower().encode()
    m = hashlib.md5(member_email)
    return m.hexdigest()