def create_locks(context, network_ids, addresses):
    """Creates locks for each IP address that is null-routed.

    The function creates the IP address if it is not present in the database.

    """

    for address in addresses:
        address_model = None
        try:
            address_model = _find_or_create_address(
                context, network_ids, address)
            lock_holder = None
            if address_model.lock_id:
                lock_holder = db_api.lock_holder_find(
                    context,
                    lock_id=address_model.lock_id, name=LOCK_NAME,
                    scope=db_api.ONE)

            if not lock_holder:
                LOG.info("Creating lock holder on IPAddress %s with id %s",
                         address_model.address_readable,
                         address_model.id)
                db_api.lock_holder_create(
                    context, address_model, name=LOCK_NAME, type="ip_address")
        except Exception:
            LOG.exception("Failed to create lock holder on IPAddress %s",
                          address_model)
            continue
    context.session.flush()