def image(self, src, title, text):
        """Rendering a image with title and text.

        :param src: source link of the image.
        :param title: title text of the image.
        :param text: alt text of the image.
        """
        # rst does not support title option
        # and I couldn't find title attribute in HTML standard
        return '\n'.join([
            '',
            '.. image:: {}'.format(src),
            '   :target: {}'.format(src),
            '   :alt: {}'.format(text),
            '',
        ])