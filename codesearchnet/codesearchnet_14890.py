def update_terminal_colors(self):
        """
        Update terminal color scheme based on the pygments color scheme colors
        """
        self.color_scheme = self.create_color_scheme(
            background=self.syntax_highlighter.color_scheme.background,
            foreground=self.syntax_highlighter.color_scheme.formats['normal'].foreground().color())