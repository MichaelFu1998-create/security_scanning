def _aggregations_process(aggregation_types=None,
                          start_date=None, end_date=None,
                          update_bookmark=False, eager=False):
    """Process stats aggregations."""
    aggregation_types = (aggregation_types or
                         list(current_stats.enabled_aggregations))
    if eager:
        aggregate_events.apply(
            (aggregation_types,),
            dict(start_date=start_date, end_date=end_date,
                 update_bookmark=update_bookmark),
            throw=True)
        click.secho('Aggregations processed successfully.', fg='green')
    else:
        aggregate_events.delay(
            aggregation_types, start_date=start_date, end_date=end_date)
        click.secho('Aggregations processing task sent...', fg='yellow')