def get_all(self, include_archived=False):
        """Get all the conversations.

        Args:
            include_archived (bool): (optional) Whether to include archived
                conversations. Defaults to ``False``.

        Returns:
            List of all :class:`.Conversation` objects.
        """
        return [conv for conv in self._conv_dict.values()
                if not conv.is_archived or include_archived]