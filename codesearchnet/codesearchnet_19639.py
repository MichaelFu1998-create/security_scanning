def render(self, template, **data):
        """Render data with template, return html unicodes.
        parameters
          template   str  the template's filename
          data       dict the data to render
        """
        # make a copy and update the copy
        dct = self.global_data.copy()
        dct.update(data)

        try:
            html = self.env.get_template(template).render(**dct)
        except TemplateNotFound:
            raise JinjaTemplateNotFound
        return html