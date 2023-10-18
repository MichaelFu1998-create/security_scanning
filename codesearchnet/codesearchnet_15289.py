def _make_session(connection: Optional[str] = None) -> Session:
    """Make a session."""
    if connection is None:
        connection = get_global_connection()

    engine = create_engine(connection)

    create_all(engine)

    session_cls = sessionmaker(bind=engine)
    session = session_cls()

    return session