def post_publication_processing(event, cursor):
    """Process post-publication events coming out of the database."""
    module_ident, ident_hash = event.module_ident, event.ident_hash

    celery_app = get_current_registry().celery_app

    # Check baking is not already queued.
    cursor.execute('SELECT result_id::text '
                   'FROM document_baking_result_associations '
                   'WHERE module_ident = %s', (module_ident,))
    for result in cursor.fetchall():
        state = celery_app.AsyncResult(result[0]).state
        if state in ('QUEUED', 'STARTED', 'RETRY'):
            logger.debug('Already queued module_ident={} ident_hash={}'.format(
                module_ident, ident_hash))
            return

    logger.debug('Queued for processing module_ident={} ident_hash={}'.format(
        module_ident, ident_hash))
    recipe_ids = _get_recipe_ids(module_ident, cursor)
    update_module_state(cursor, module_ident, 'processing', recipe_ids[0])
    # Commit the state change before preceding.
    cursor.connection.commit()

    # Start of task
    # FIXME Looking up the task isn't the most clear usage here.
    task_name = 'cnxpublishing.subscribers.baking_processor'
    baking_processor = celery_app.tasks[task_name]
    result = baking_processor.delay(module_ident, ident_hash)
    baking_processor.backend.store_result(result.id, None, 'QUEUED')

    # Save the mapping between a celery task and this event.
    track_baking_proc_state(result, module_ident, cursor)