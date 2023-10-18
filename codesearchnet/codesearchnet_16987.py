def register_templates():
    """Register elasticsearch templates for events."""
    event_templates = [current_stats._events_config[e]
                       ['templates']
                       for e in
                       current_stats._events_config]
    aggregation_templates = [current_stats._aggregations_config[a]
                             ['templates']
                             for a in
                             current_stats._aggregations_config]
    return event_templates + aggregation_templates