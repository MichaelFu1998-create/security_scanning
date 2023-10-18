def render(self):
        """
        Renders configuration by using the jinja2 templating engine
        """
        # get jinja2 template
        template_name = '{0}.jinja2'.format(self.get_name())
        template = self.template_env.get_template(template_name)
        # render template and cleanup
        context = getattr(self.backend, 'intermediate_data', {})
        output = template.render(data=context)
        return self.cleanup(output)