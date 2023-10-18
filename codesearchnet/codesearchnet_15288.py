def _store_helper(model: Action, session: Optional[Session] = None) -> None:
    """Help store an action."""
    if session is None:
        session = _make_session()

    session.add(model)
    session.commit()
    session.close()