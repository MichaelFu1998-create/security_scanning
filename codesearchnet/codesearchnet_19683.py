def _store(self, messages, response, *args, **kwargs):
        """
        persistent messages are already in the database inside the 'archive',
        so we can say they're already "stored".
        Here we put them in the inbox, or remove from the inbox in case the
        messages were iterated.

        messages contains only new msgs if self.used==True
        else contains both new and unread messages
        """
        contrib_messages = []
        if self.user.is_authenticated():
            if not messages:
                # erase inbox
                self.backend.inbox_purge(self.user)
            else:
                for m in messages:
                    try:
                        self.backend.inbox_store([self.user], m)
                    except MessageTypeNotSupported:
                        contrib_messages.append(m)

        super(StorageMixin, self)._store(contrib_messages, response, *args, **kwargs)