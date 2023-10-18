def count(cls, session: Optional[Session] = None) -> int:
        """Count all actions."""
        if session is None:
            session = _make_session()

        count = session.query(cls).count()
        session.close()
        return count