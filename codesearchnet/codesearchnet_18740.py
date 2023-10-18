def render_oembed(self, oembed_resource, original_url, template_dir=None,
                      context=None):
        """
        Render the oembed resource and return as a string.
        
        Template directory will always fall back to 'oembed/[type].html', but
        a custom template dir can be passed in using the kwargs.
        
        Templates are given two context variables:
        - response: an OEmbedResource
        - original_url: the url that was passed to the consumer
        """
        provided_context = context or Context()
        context = RequestContext(context.get("request") or mock_request())
        context.update(provided_context)
        
        # templates are named for the resources they display, i.e. video.html
        template_name = '%s.html' % oembed_resource.type
        
        # set up template finder to fall back to the link template
        templates = [os.path.join('oembed', template_name), 'oembed/link.html']
        
        # if there's a custom template dir, look there first
        if template_dir:
            templates.insert(0, os.path.join('oembed', template_dir, template_name))
        
        template = select_template(templates)
        
        context.push()
        context['response'] = oembed_resource
        context['original_url'] = original_url
        rendered = template.render(context)
        context.pop()
        
        return rendered.strip()