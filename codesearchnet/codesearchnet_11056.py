def content(self, attributes: List[str]):
        """Build content tuple for the buffer"""
        formats = []
        attrs = []
        for attrib_format, attrib in zip(self.attrib_formats, self.attributes):

            if attrib not in attributes:
                formats.append(attrib_format.pad_str())
                continue

            formats.append(attrib_format.format)
            attrs.append(attrib)

            attributes.remove(attrib)

        if not attrs:
            return None

        return (
            self.buffer,
            "{}{}".format(" ".join(formats), '/i' if self.per_instance else ''),
            *attrs
        )