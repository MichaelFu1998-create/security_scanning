def generate_hub_key(resolver_id, hub_id, repository_id, entity_type, entity_id=None):
    """Create and return an array of hub keys
    :param resolver_id: the service that can resolve this key
    :param hub_id: the unique id of the hub
    :param repository_id: the type of id that the provider recognises
    :param entity_type: the type of the entity to which the key refers.
    :param entity_id: ID of entity (UUID)
    :returns: a hub key
    :raises:
    :AttributeError: if a parameter has a bad value
    :TypeError: if a parameter has a bad value
    :ValueError: if a parameter has a bad value
    """
    parsed = urlparse(resolver_id)
    if not parsed.scheme:
        parsed = parsed._replace(scheme=PROTOCOL, netloc=idna_encode(parsed.path.lower()), path=u'')
    else:
        parsed = parsed._replace(netloc=idna_encode(parsed.netloc.lower()))

    resolver_id = urlunparse(parsed)

    hub_id = url_quote(hub_id.lower())

    if not entity_id:
        entity_id = str(uuid.uuid4()).replace('-', '')
    else:
        match_part(entity_id, 'entity_id')

    # If any of these checks fail a ValueError exception is raised
    match_part(resolver_id, 'resolver_id')
    match_part(hub_id, 'hub_id')
    match_part(repository_id, 'repository_id')
    match_part(entity_type, 'entity_type')

    hub_key = SEPARATOR.join(
        [resolver_id, SCHEMA, hub_id, repository_id, entity_type, entity_id])
    return hub_key