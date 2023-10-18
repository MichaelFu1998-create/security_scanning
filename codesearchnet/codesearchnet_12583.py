async def get_session(cls, view):
        """
        Every request have a session instance
        :param view:
        :return:
        """
        session = cls(view)
        session.key = await session.get_key()
        session._data = await session.load() or {}
        return session