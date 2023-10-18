def transform_description(self, content_metadata_item):
        """
        Return the transformed version of the course description.

        We choose one value out of the course's full description, short description, and title
        depending on availability and length limits.
        """
        full_description = content_metadata_item.get('full_description') or ''
        if 0 < len(full_description) <= self.LONG_STRING_LIMIT:  # pylint: disable=len-as-condition
            return full_description
        return content_metadata_item.get('short_description') or content_metadata_item.get('title') or ''