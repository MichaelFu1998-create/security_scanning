def _aggregations_list_bookmarks(aggregation_types=None,
                                 start_date=None, end_date=None, limit=None):
    """List aggregation bookmarks."""
    aggregation_types = (aggregation_types or
                         list(current_stats.enabled_aggregations))
    for a in aggregation_types:
        aggr_cfg = current_stats.aggregations[a]
        aggregator = aggr_cfg.aggregator_class(
            name=aggr_cfg.name, **aggr_cfg.aggregator_config)
        bookmarks = aggregator.list_bookmarks(start_date, end_date, limit)
        click.echo('{}:'.format(a))
        for b in bookmarks:
            click.echo(' - {}'.format(b.date))