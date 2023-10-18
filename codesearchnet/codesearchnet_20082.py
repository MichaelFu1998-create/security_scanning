async def from_api_token(cls, token=None, api_cls=SlackBotApi):
        """Create a new instance from the API token.

        Arguments:
          token (:py:class:`str`, optional): The bot's API token
            (defaults to ``None``, which means looking in the
            environment).
          api_cls (:py:class:`type`, optional): The class to create
            as the ``api`` argument for API access (defaults to
            :py:class:`aslack.slack_api.SlackBotApi`).

        Returns:
          :py:class:`SlackBot`: The new instance.

        """
        api = api_cls.from_env() if token is None else api_cls(api_token=token)
        data = await api.execute_method(cls.API_AUTH_ENDPOINT)
        return cls(data['user_id'], data['user'], api)