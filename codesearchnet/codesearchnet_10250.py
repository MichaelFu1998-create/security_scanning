def check_known_schemas(self):
        """\
        checks to see if we were able to find the image via known schemas:

        Supported Schemas
         - Open Graph
         - schema.org
        """
        if 'image' in self.article.opengraph:
            return self.get_image(self.article.opengraph["image"],
                                  extraction_type='opengraph')
        elif (self.article.schema and 'image' in self.article.schema and
              "url" in self.article.schema["image"]):
            return self.get_image(self.article.schema["image"]["url"],
                                  extraction_type='schema.org')
        return None