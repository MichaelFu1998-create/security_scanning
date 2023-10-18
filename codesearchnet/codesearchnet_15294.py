def ls(cls, session: Optional[Session] = None) -> List['Action']:
        """Get all actions."""
        if session is None:
            session = _make_session()

        actions = session.query(cls).order_by(cls.created.desc()).all()
        session.close()
        return actions