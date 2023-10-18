def delete_segment_allocation_range(context, sa_id):
    """Delete a segment_allocation_range.

    : param context: neutron api request context
    : param id: UUID representing the segment_allocation_range to delete.
    """
    LOG.info("delete_segment_allocation_range %s for tenant %s" %
             (sa_id, context.tenant_id))
    if not context.is_admin:
        raise n_exc.NotAuthorized()

    with context.session.begin():
        sa_range = db_api.segment_allocation_range_find(
            context, id=sa_id, scope=db_api.ONE)
        if not sa_range:
            raise q_exc.SegmentAllocationRangeNotFound(
                segment_allocation_range_id=sa_id)
        _delete_segment_allocation_range(context, sa_range)