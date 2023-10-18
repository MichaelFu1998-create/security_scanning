def codespan(self, text):
        """Rendering inline `code` text.

        :param text: text content for inline code.
        """
        if '``' not in text:
            return '\ ``{}``\ '.format(text)
        else:
            # actually, docutils split spaces in literal
            return self._raw_html(
                '<code class="docutils literal">'
                '<span class="pre">{}</span>'
                '</code>'.format(text.replace('`', '&#96;')))