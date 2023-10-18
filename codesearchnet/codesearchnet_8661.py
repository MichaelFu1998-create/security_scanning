def transform_image(self, content_metadata_item):
        """
        Return the image URI of the content item.
        """
        image_url = ''
        if content_metadata_item['content_type'] in ['course', 'program']:
            image_url = content_metadata_item.get('card_image_url')
        elif content_metadata_item['content_type'] == 'courserun':
            image_url = content_metadata_item.get('image_url')

        return image_url