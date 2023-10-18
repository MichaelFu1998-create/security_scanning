def delete_locks(context, network_ids, addresses):
    """Deletes locks for each IP address that is no longer null-routed."""
    addresses_no_longer_null_routed = _find_addresses_to_be_unlocked(
        context, network_ids, addresses)
    LOG.info("Deleting %s lock holders on IPAddress with ids: %s",
             len(addresses_no_longer_null_routed),
             [addr.id for addr in addresses_no_longer_null_routed])

    for address in addresses_no_longer_null_routed:
        lock_holder = None
        try:
            lock_holder = db_api.lock_holder_find(
                context, lock_id=address.lock_id, name=LOCK_NAME,
                scope=db_api.ONE)
            if lock_holder:
                db_api.lock_holder_delete(context, address, lock_holder)
        except Exception:
            LOG.exception("Failed to delete lock holder %s", lock_holder)
            continue
    context.session.flush()