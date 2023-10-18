def output_image_link(self, m):
        """Pass through rest role."""
        return self.renderer.image_link(
            m.group('url'), m.group('target'), m.group('alt'))