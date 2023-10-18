def render_subject(self, context):
        """
        Renders the message subject for the given context.

        The context data is automatically unescaped to avoid rendering HTML
        entities in ``text/plain`` content.

        :param context: The context to use when rendering the subject template.
        :type context: :class:`~django.template.Context`
        :returns: A rendered subject.
        :rtype: :class:`str`
        """
        rendered = self.subject_template.render(unescape(context))
        return rendered.strip()