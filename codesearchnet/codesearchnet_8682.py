def export(self):
        """
        Return the exported and transformed content metadata as a dictionary.
        """
        content_metadata_export = {}
        content_metadata_items = self.enterprise_api.get_content_metadata(self.enterprise_customer)
        LOGGER.info('Retrieved content metadata for enterprise [%s]', self.enterprise_customer.name)
        for item in content_metadata_items:
            transformed = self._transform_item(item)
            LOGGER.info(
                'Exporting content metadata item with plugin configuration [%s]: [%s]',
                self.enterprise_configuration,
                json.dumps(transformed, indent=4),
            )
            content_metadata_item_export = ContentMetadataItemExport(item, transformed)
            content_metadata_export[content_metadata_item_export.content_id] = content_metadata_item_export
        return OrderedDict(sorted(content_metadata_export.items()))