def segment_allocation_find(context, lock_mode=False, **filters):
    """Query for segment allocations."""
    range_ids = filters.pop("segment_allocation_range_ids", None)

    query = context.session.query(models.SegmentAllocation)
    if lock_mode:
        query = query.with_lockmode("update")

    query = query.filter_by(**filters)

    # Optionally filter by given list of range ids
    if range_ids:
        query.filter(
            models.SegmentAllocation.segment_allocation_range_id.in_(
                range_ids))
    return query