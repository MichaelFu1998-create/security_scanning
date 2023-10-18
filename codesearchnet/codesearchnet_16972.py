def _aggregations_delete(aggregation_types=None,
                         start_date=None, end_date=None):
    """Delete computed aggregations."""
    aggregation_types = (aggregation_types or
                         list(current_stats.enabled_aggregations))
    for a in aggregation_types:
        aggr_cfg = current_stats.aggregations[a]
        aggregator = aggr_cfg.aggregator_class(
            name=aggr_cfg.name, **aggr_cfg.aggregator_config)
        aggregator.delete(start_date, end_date)