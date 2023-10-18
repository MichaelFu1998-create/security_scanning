def extract_oembeds(self, text, maxwidth=None, maxheight=None, resource_type=None):
        """
        Scans a block of text and extracts oembed data on any urls,
        returning it in a list of dictionaries
        """
        parser = text_parser()
        urls = parser.extract_urls(text)
        return self.handle_extracted_urls(urls, maxwidth, maxheight, resource_type)