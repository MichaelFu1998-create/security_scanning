def render_to_message(self, extra_context=None, *args, **kwargs):
        """
        Renders and returns an unsent message with the given context.

        Any extra keyword arguments passed will be passed through as keyword
        arguments to the message constructor.

        :param extra_context: Any additional context to use when rendering
            templated content.
        :type extra_context: :class:`dict`
        :returns: A message instance.
        :rtype: :attr:`.message_class`
        """
        message = super(TemplatedHTMLEmailMessageView, self)\
            .render_to_message(extra_context, *args, **kwargs)

        if extra_context is None:
            extra_context = {}

        context = self.get_context_data(**extra_context)
        content = self.render_html_body(context)
        message.attach_alternative(content, mimetype='text/html')
        return message