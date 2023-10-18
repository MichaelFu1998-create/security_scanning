def output_eol_literal_marker(self, m):
        """Pass through rest link."""
        marker = ':' if m.group(1) is None else ''
        return self.renderer.eol_literal_marker(marker)