def send(self, extra_context=None, **kwargs):
        """
        Renders and sends an email message.

        All keyword arguments other than ``extra_context`` are passed through
        as keyword arguments when constructing a new :attr:`message_class`
        instance for this message.

        This method exists primarily for convenience, and the proper
        rendering of your message should not depend on the behavior of this
        method. To alter how a message is created, override
        :meth:``render_to_message`` instead, since that should always be
        called, even if a message is not sent.

        :param extra_context: Any additional context data that will be used
            when rendering this message.
        :type extra_context: :class:`dict`
        """
        message = self.render_to_message(extra_context=extra_context, **kwargs)
        return message.send()