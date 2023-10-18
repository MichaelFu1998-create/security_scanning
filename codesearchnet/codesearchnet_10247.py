def is_valid_filename(self, image_node):
        """\
        will check the image src against a list
        of bad image files we know of like buttons, etc...
        """
        src = self.parser.getAttribute(image_node, attr='src')

        if not src:
            return False

        if self.badimages_names_re.search(src):
            return False

        return True