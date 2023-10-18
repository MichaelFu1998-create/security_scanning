def declare_queues():
    """Index statistics events."""
    return [dict(name='stats-{0}'.format(event['event_type']),
                 exchange=current_stats.exchange)
            for event in current_stats._events_config.values()]