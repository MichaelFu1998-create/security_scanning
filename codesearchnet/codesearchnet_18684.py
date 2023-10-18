def html_to_text(cls, html):
        """Return stripped HTML, keeping only MathML."""
        s = cls()
        s.feed(html)
        unescaped_data = s.unescape(s.get_data())
        return escape_for_xml(unescaped_data, tags_to_keep=s.mathml_elements)