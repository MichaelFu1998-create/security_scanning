def _get_lookup_spec(identifier):
    """Return EntityLookupSpec from phone number, email address, or gaia ID."""
    if identifier.startswith('+'):
        return hangups.hangouts_pb2.EntityLookupSpec(
            phone=identifier, create_offnetwork_gaia=True
        )
    elif '@' in identifier:
        return hangups.hangouts_pb2.EntityLookupSpec(
            email=identifier, create_offnetwork_gaia=True
        )
    else:
        return hangups.hangouts_pb2.EntityLookupSpec(gaia_id=identifier)