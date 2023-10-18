def render_to_message(self, extra_context=None, **kwargs):
        """
        Renders and returns an unsent message with the provided context.

        Any extra keyword arguments passed will be passed through as keyword
        arguments to the message constructor.

        :param extra_context: Any additional context to use when rendering the
            templated content.
        :type extra_context: :class:`dict`
        :returns: A message instance.
        :rtype: :attr:`.message_class`
        """
        if extra_context is None:
            extra_context = {}

        # Ensure our custom headers are added to the underlying message class.
        kwargs.setdefault('headers', {}).update(self.headers)

        context = self.get_context_data(**extra_context)
        return self.message_class(
            subject=self.render_subject(context),
            body=self.render_body(context),
            **kwargs)