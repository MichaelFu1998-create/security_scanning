def register_events():
    """Register sample events."""
    return [
        dict(
            event_type='file-download',
            templates='invenio_stats.contrib.file_download',
            processor_class=EventsIndexer,
            processor_config=dict(
                preprocessors=[
                    flag_robots,
                    anonymize_user,
                    build_file_unique_id
                ])),
        dict(
            event_type='record-view',
            templates='invenio_stats.contrib.record_view',
            processor_class=EventsIndexer,
            processor_config=dict(
                preprocessors=[
                    flag_robots,
                    anonymize_user,
                    build_record_unique_id
                ]))
    ]