def get_content_id(self, content_metadata_item):
        """
        Return the id for the given content_metadata_item, `uuid` for programs or `key` for other content
        """
        content_id = content_metadata_item.get('key', '')
        if content_metadata_item['content_type'] == 'program':
            content_id = content_metadata_item.get('uuid', '')
        return content_id