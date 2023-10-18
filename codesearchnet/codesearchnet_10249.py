def check_link_tag(self):
        """\
        checks to see if we were able to
        find open link_src on this page
        """
        node = self.article.raw_doc
        meta = self.parser.getElementsByTag(node, tag='link', attr='rel', value='image_src')
        for item in meta:
            src = self.parser.getAttribute(item, attr='href')
            if src:
                return self.get_image(src, extraction_type='linktag')
        return None