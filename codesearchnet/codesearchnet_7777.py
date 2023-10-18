def write(self, album):
        """Generate the HTML page and save it."""

        page = self.template.render(**self.generate_context(album))
        output_file = os.path.join(album.dst_path, album.output_file)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(page)