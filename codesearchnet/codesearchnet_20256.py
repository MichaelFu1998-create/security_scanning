def add_group_name_alias(self, groupName, aliasName):
        """
        Creates secondary name(s) for group names. Once an alias is created the
        group name cannot be used to request HTTP playback of that stream. Once
        an alias is used (requested by a client) the alias is removed. Aliases
        are designed to be used to protect/hide your source streams.

        :param groupName: The original group name
        :type groupName: str

        :param aliasName: The alias alternative to the group name
        :type aliasName: str

        :link: http://docs.evostream.com/ems_api_definition/addgroupnamealias
        """
        return self.protocol.execute('addGroupNameAlias', groupName=groupName,
                                     aliasName=aliasName)