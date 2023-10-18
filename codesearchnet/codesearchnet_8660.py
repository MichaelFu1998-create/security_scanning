def transform_description(self, content_metadata_item):
        """
        Return the description of the content item.
        """
        description_with_locales = []

        for locale in self.enterprise_configuration.get_locales():
            description_with_locales.append({
                'locale': locale,
                'value': (
                    content_metadata_item.get('full_description') or
                    content_metadata_item.get('short_description') or
                    content_metadata_item.get('title', '')
                )
            })

        return description_with_locales