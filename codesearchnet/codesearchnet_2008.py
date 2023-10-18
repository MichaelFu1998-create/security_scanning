def _format_text(self, text):
        """
        Format a paragraph of free-form text for inclusion in the
        help output at the current indentation level.
        """
        text_width = max(self.width - self.current_indent, 11)
        indent = " "*self.current_indent
        return textwrap.fill(text,
                             text_width,
                             initial_indent=indent,
                             subsequent_indent=indent)