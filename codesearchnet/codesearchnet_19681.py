def _get(self, *args, **kwargs):
        """
        Retrieve unread messages for current user, both from the inbox and
        from other storages
        """
        messages, all_retrieved = super(StorageMixin, self)._get(*args, **kwargs)
        if self.user.is_authenticated():
            inbox_messages = self.backend.inbox_list(self.user)
        else:
            inbox_messages = []

        return messages + inbox_messages, all_retrieved