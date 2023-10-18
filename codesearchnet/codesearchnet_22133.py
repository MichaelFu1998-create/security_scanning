def from_server(cls, server, slug):
        """Retrieve a challenge from the MapRoulette server
        :type server
        """

        challenge = server.get(
            'challenge',
            replacements={'slug': slug})
        return cls(
            **challenge)