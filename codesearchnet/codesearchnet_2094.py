def link(self, link, title, text):
        """Rendering a given link with content and title.

        :param link: href link for ``<a>`` tag.
        :param title: title content for `title` attribute.
        :param text: text content for description.
        """
        if title:
            raise NotImplementedError('sorry')
        return '\ `{text} <{target}>`_\ '.format(target=link, text=text)