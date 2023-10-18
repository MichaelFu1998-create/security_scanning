def anonymize_user(doc):
    """Preprocess an event by anonymizing user information.

    The anonymization is done by removing fields that can uniquely identify a
    user, such as the user's ID, session ID, IP address and User Agent, and
    hashing them to produce a ``visitor_id`` and ``unique_session_id``. To
    further secure the method, a randomly generated 32-byte salt is used, that
    expires after 24 hours and is discarded. The salt values are stored in
    Redis (or whichever backend Invenio-Cache uses). The ``unique_session_id``
    is calculated in the same way as the ``visitor_id``, with the only
    difference that it also takes into account the hour of the event . All of
    these rules effectively mean that a user can have a unique ``visitor_id``
    for each day and unique ``unique_session_id`` for each hour of a day.

    This session ID generation process was designed according to the `Project
    COUNTER Code of Practice <https://www.projectcounter.org/code-of-
    practice-sections/general-information/>`_.

    In addition to that the country of the user is extracted from the IP
    address as a ISO 3166-1 alpha-2 two-letter country code (e.g. "CH" for
    Switzerland).
    """
    ip = doc.pop('ip_address', None)
    if ip:
        doc.update({'country': get_geoip(ip)})

    user_id = doc.pop('user_id', '')
    session_id = doc.pop('session_id', '')
    user_agent = doc.pop('user_agent', '')

    # A 'User Session' is defined as activity by a user in a period of
    # one hour. timeslice represents the hour of the day in which
    # the event has been generated and together with user info it determines
    # the 'User Session'
    timestamp = arrow.get(doc.get('timestamp'))
    timeslice = timestamp.strftime('%Y%m%d%H')
    salt = get_anonymization_salt(timestamp)

    visitor_id = hashlib.sha224(salt.encode('utf-8'))
    # TODO: include random salt here, that changes once a day.
    # m.update(random_salt)
    if user_id:
        visitor_id.update(user_id.encode('utf-8'))
    elif session_id:
        visitor_id.update(session_id.encode('utf-8'))
    elif ip and user_agent:
        vid = '{}|{}|{}'.format(ip, user_agent, timeslice)
        visitor_id.update(vid.encode('utf-8'))
    else:
        # TODO: add random data?
        pass

    unique_session_id = hashlib.sha224(salt.encode('utf-8'))
    if user_id:
        sid = '{}|{}'.format(user_id, timeslice)
        unique_session_id.update(sid.encode('utf-8'))
    elif session_id:
        sid = '{}|{}'.format(session_id, timeslice)
        unique_session_id.update(sid.encode('utf-8'))
    elif ip and user_agent:
        sid = '{}|{}|{}'.format(ip, user_agent, timeslice)
        unique_session_id.update(sid.encode('utf-8'))

    doc.update(dict(
        visitor_id=visitor_id.hexdigest(),
        unique_session_id=unique_session_id.hexdigest()
    ))

    return doc