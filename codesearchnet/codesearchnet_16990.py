def aggregate_events(aggregations, start_date=None, end_date=None,
                     update_bookmark=True):
    """Aggregate indexed events."""
    start_date = dateutil_parse(start_date) if start_date else None
    end_date = dateutil_parse(end_date) if end_date else None
    results = []
    for a in aggregations:
        aggr_cfg = current_stats.aggregations[a]
        aggregator = aggr_cfg.aggregator_class(
            name=aggr_cfg.name, **aggr_cfg.aggregator_config)
        results.append(aggregator.run(start_date, end_date, update_bookmark))
    return results