def _events_process(event_types=None, eager=False):
    """Process stats events."""
    event_types = event_types or list(current_stats.enabled_events)
    if eager:
        process_events.apply((event_types,), throw=True)
        click.secho('Events processed successfully.', fg='green')
    else:
        process_events.delay(event_types)
        click.secho('Events processing task sent...', fg='yellow')