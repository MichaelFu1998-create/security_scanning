def render_to(self, path, template, **data):
        """Render data with template and then write to path"""
        html = self.render(template, **data)
        with open(path, 'w') as f:
            f.write(html.encode(charset))