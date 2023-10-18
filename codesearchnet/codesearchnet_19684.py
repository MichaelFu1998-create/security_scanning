def _prepare_messages(self, messages):
        """
        Like the base class method, prepares a list of messages for storage
        but avoid to do this for `models.Message` instances.
        """
        for message in messages:
            if not self.backend.can_handle(message):
                message._prepare()