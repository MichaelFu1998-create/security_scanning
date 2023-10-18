def get(self, request, template_id, view_type):
        """
        Render the given template with the stock data.
        """
        template = get_object_or_404(EnrollmentNotificationEmailTemplate, pk=template_id)
        if view_type not in self.view_type_contexts:
            return HttpResponse(status=404)
        base_context = self.view_type_contexts[view_type].copy()
        base_context.update({'user_name': self.get_user_name(request)})
        return HttpResponse(template.render_html_template(base_context), content_type='text/html')