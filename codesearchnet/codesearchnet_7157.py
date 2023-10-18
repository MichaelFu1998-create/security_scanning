async def lookup_entities(client, args):
    """Search for entities by phone number, email, or gaia_id."""
    lookup_spec = _get_lookup_spec(args.entity_identifier)
    request = hangups.hangouts_pb2.GetEntityByIdRequest(
        request_header=client.get_request_header(),
        batch_lookup_spec=[lookup_spec],
    )
    res = await client.get_entity_by_id(request)

    # Print the list of entities in the response.
    for entity_result in res.entity_result:
        for entity in entity_result.entity:
            print(entity)