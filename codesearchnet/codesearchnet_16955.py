def register_receivers(app, config):
    """Register signal receivers which send events."""
    for event_name, event_config in config.items():
        event_builders = [
            obj_or_import_string(func)
            for func in event_config.get('event_builders', [])
        ]

        signal = obj_or_import_string(event_config['signal'])
        signal.connect(
            EventEmmiter(event_name, event_builders), sender=app, weak=False
        )