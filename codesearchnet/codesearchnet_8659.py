def transform_title(self, content_metadata_item):
        """
        Return the title of the content item.
        """
        title_with_locales = []

        for locale in self.enterprise_configuration.get_locales():
            title_with_locales.append({
                'locale': locale,
                'value': content_metadata_item.get('title', '')
            })

        return title_with_locales