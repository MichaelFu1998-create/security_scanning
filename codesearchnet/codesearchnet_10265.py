def get_title(self):
        """\
        Fetch the article title and analyze it
        """
        title = ''

        # rely on opengraph in case we have the data
        if "title" in list(self.article.opengraph.keys()):
            return self.clean_title(self.article.opengraph['title'])
        elif self.article.schema and "headline" in self.article.schema:
            return self.clean_title(self.article.schema['headline'])

        # try to fetch the meta headline
        meta_headline = self.parser.getElementsByTag(self.article.doc,
                                                     tag="meta",
                                                     attr="name",
                                                     value="headline")
        if meta_headline is not None and len(meta_headline) > 0:
            title = self.parser.getAttribute(meta_headline[0], 'content')
            return self.clean_title(title)

        # otherwise use the title meta
        title_element = self.parser.getElementsByTag(self.article.doc, tag='title')
        if title_element is not None and len(title_element) > 0:
            title = self.parser.getText(title_element[0])
            return self.clean_title(title)

        return title