def render_html(self, obj, context=None):
        """
        Generate the 'html' attribute of an oembed resource using a template.
        Sort of a corollary to the parser's render_oembed method.  By default,
        the current mapping will be passed in as the context.
        
        OEmbed templates are stored in:
        
        oembed/provider/[app_label]_[model].html
        
        -- or --
        
        oembed/provider/media_video.html
        """        
        provided_context = context or Context()
        context = RequestContext(mock_request())
        context.update(provided_context)
        
        context.push()
        context[self._meta.context_varname] = obj
        rendered = render_to_string(self._meta.template_name, context)
        context.pop()
        return rendered