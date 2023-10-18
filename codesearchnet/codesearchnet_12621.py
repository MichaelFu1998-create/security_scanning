def render_to_response(self, context, **response_kwargs):
        """
        Returns a response with a template depending if the request is ajax 
        or not and it renders with the given context.
        """
        if self.request.is_ajax():
            template = self.page_template
        else:
            template = self.get_template_names()
        return self.response_class(
            request=self.request,
            template=template,
            context=context,
            **response_kwargs
        )