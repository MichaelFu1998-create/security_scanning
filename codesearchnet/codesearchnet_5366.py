def to_html_string(self):
        """
        Returns an etree HTML node with a document describing the process. This
        is only supported if the editor provided an SVG representation.
        """
        html = ET.Element('html')
        head = ET.SubElement(html, 'head')
        title = ET.SubElement(head, 'title')
        title.text = self.description
        body = ET.SubElement(html, 'body')
        h1 = ET.SubElement(body, 'h1')
        h1.text = self.description
        span = ET.SubElement(body, 'span')
        span.text = '___CONTENT___'

        html_text = ET.tostring(html)

        svg_content = ''
        svg_done = set()
        for spec in self.get_specs_depth_first():
            if spec.svg and spec.svg not in svg_done:
                svg_content += '<p>' + spec.svg + "</p>"
                svg_done.add(spec.svg)
        return html_text.replace('___CONTENT___', svg_content)