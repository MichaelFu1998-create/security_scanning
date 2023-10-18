def transform_courserun_description(self, content_metadata_item):
        """
        Return the description of the courserun content item.
        """
        description_with_locales = []
        content_metadata_language_code = transform_language_code(content_metadata_item.get('content_language', ''))
        for locale in self.enterprise_configuration.get_locales(default_locale=content_metadata_language_code):
            description_with_locales.append({
                'locale': locale,
                'value': (
                    content_metadata_item['full_description'] or
                    content_metadata_item['short_description'] or
                    content_metadata_item['title'] or
                    ''
                )
            })

        return description_with_locales