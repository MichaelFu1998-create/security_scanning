def _transform_item(self, content_metadata_item):
        """
        Transform the provided content metadata item to the schema expected by the integrated channel.
        """
        content_metadata_type = content_metadata_item['content_type']
        transformed_item = {}
        for integrated_channel_schema_key, edx_data_schema_key in self.DATA_TRANSFORM_MAPPING.items():
            # Look for transformer functions defined on subclasses.
            # Favor content type-specific functions.
            transformer = (
                getattr(
                    self,
                    'transform_{content_type}_{edx_data_schema_key}'.format(
                        content_type=content_metadata_type,
                        edx_data_schema_key=edx_data_schema_key
                    ),
                    None
                )
                or
                getattr(
                    self,
                    'transform_{edx_data_schema_key}'.format(
                        edx_data_schema_key=edx_data_schema_key
                    ),
                    None
                )
            )
            if transformer:
                transformed_item[integrated_channel_schema_key] = transformer(content_metadata_item)
            else:
                # The concrete subclass does not define an override for the given field,
                # so just use the data key to index the content metadata item dictionary.
                try:
                    transformed_item[integrated_channel_schema_key] = content_metadata_item[edx_data_schema_key]
                except KeyError:
                    # There may be a problem with the DATA_TRANSFORM_MAPPING on
                    # the concrete subclass or the concrete subclass does not implement
                    # the appropriate field tranformer function.
                    LOGGER.exception(
                        'Failed to transform content metadata item field [%s] for [%s]: [%s]',
                        edx_data_schema_key,
                        self.enterprise_customer.name,
                        content_metadata_item,
                    )

        return transformed_item