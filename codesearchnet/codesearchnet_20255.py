def add_stream_alias(self, localStreamName, aliasName, **kwargs):
        """
        Allows you to create secondary name(s) for internal streams. Once an
        alias is created the localstreamname cannot be used to request
        playback of that stream. Once an alias is used (requested by a client)
        the alias is removed. Aliases are designed to be used to protect/hide
        your source streams.

        :param localStreamName: The original stream name
        :type localStreamName: str

        :param aliasName: The alias alternative to the localStreamName
        :type aliasName: str

        :param expirePeriod: The expiration period for this alias. Negative
            values will be treated as one-shot but no longer than the absolute
            positive value in seconds, 0 means it will not expire, positive
            values mean the alias can be used multiple times but expires after
            this many seconds. The default is -600 (one-shot, 10 mins)
        :type expirePeriod: int

        :link: http://docs.evostream.com/ems_api_definition/addstreamalias
        """
        return self.protocol.execute('addStreamAlias',
                                     localStreamName=localStreamName,
                                     aliasName=aliasName, **kwargs)