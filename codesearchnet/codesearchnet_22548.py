def includeme(config):
    """
    Initialize the model for a Pyramid app.

    Activate this setup using ``config.include('baka_model')``.

    """
    settings = config.get_settings()
    should_create = asbool(settings.get('baka_model.should_create_all', False))
    should_drop = asbool(settings.get('baka_model.should_drop_all', False))

    # Configure the transaction manager to support retrying retryable
    # exceptions. We also register the session factory with the thread-local
    # transaction manager, so that all sessions it creates are registered.
    #    "tm.attempts": 3,
    config.add_settings({
        "retry.attempts": 3,
        "tm.activate_hook": tm_activate_hook,
        "tm.annotate_user": False,
    })

    # use pyramid_retry couse pyramid_tm disabled it
    config.include('pyramid_retry')
    # use pyramid_tm to hook the transaction lifecycle to the request
    config.include('pyramid_tm')

    engine = get_engine(settings)
    session_factory = get_session_factory(engine)

    config.registry['db_session_factory'] = session_factory

    # make request.db available for use in Pyramid
    config.add_request_method(
        # r.tm is the transaction manager used by pyramid_tm
        lambda r: get_tm_session(session_factory, r.tm),
        'db',
        reify=True
    )

    # service model factory
    config.include('.service')

    # Register a deferred action to bind the engine when the configuration is
    # committed. Deferring the action means that this module can be included
    # before model modules without ill effect.
    config.action(None, bind_engine, (engine,), {
        'should_create': should_create,
        'should_drop': should_drop
    }, order=10)