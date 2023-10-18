def detail_view(self, request):
        """
        Renders the message view to a response.
        """
        context = {
            'preview': self,
        }

        kwargs = {}
        if self.form_class:
            if request.GET:
                form = self.form_class(data=request.GET)
            else:
                form = self.form_class()

            context['form'] = form
            if not form.is_bound or not form.is_valid():
                return render(request, 'mailviews/previews/detail.html', context)

            kwargs.update(form.get_message_view_kwargs())

        message_view = self.get_message_view(request, **kwargs)

        message = message_view.render_to_message()
        raw = message.message()
        headers = OrderedDict((header, maybe_decode_header(raw[header])) for header in self.headers)

        context.update({
            'message': message,
            'subject': message.subject,
            'body': message.body,
            'headers': headers,
            'raw': raw.as_string(),
        })

        alternatives = getattr(message, 'alternatives', [])
        try:
            html = next(alternative[0] for alternative in alternatives
                if alternative[1] == 'text/html')
            context.update({
                'html': html,
                'escaped_html': b64encode(html.encode('utf-8')),
            })
        except StopIteration:
            pass

        return render(request, self.template_name, context)