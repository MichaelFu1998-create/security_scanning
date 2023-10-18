def process_events(event_types):
    """Index statistics events."""
    results = []
    for e in event_types:
        processor = current_stats.events[e].processor_class(
            **current_stats.events[e].processor_config)
        results.append((e, processor.run()))
    return results