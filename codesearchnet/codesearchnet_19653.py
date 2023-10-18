def parse(self, source):
        """Parse ascii post source, return dict"""

        rt, title, title_pic, markdown = libparser.parse(source)

        if rt == -1:
            raise SeparatorNotFound
        elif rt == -2:
            raise PostTitleNotFound

        # change to unicode
        title, title_pic, markdown = map(to_unicode, (title, title_pic,
                                                      markdown))

        # render to html
        html = self.markdown.render(markdown)
        summary = self.markdown.render(markdown[:200])

        return {
            'title': title,
            'markdown': markdown,
            'html': html,
            'summary': summary,
            'title_pic': title_pic
        }