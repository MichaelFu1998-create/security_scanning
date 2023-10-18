def add(self, level, message, extra_tags=''):
        """
        If the message level was configured for being stored and request.user
        is not anonymous, save it to the database. Otherwise, let some other
        class handle the message.

        Notice: controls like checking the message is not empty and the level
        is above the filter need to be performed here, but it could happen
        they'll be performed again later if the message does not need to be
        stored.
        """
        if not message:
            return
        # Check that the message level is not less than the recording level.
        level = int(level)
        if level < self.level:
            return
        # Check if the message doesn't have a level that needs to be persisted
        if level not in stored_messages_settings.STORE_LEVELS or self.user.is_anonymous():
            return super(StorageMixin, self).add(level, message, extra_tags)

        self.added_new = True
        m = self.backend.create_message(level, message, extra_tags)
        self.backend.archive_store([self.user], m)
        self._queued_messages.append(m)