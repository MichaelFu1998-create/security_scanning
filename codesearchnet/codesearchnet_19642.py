def replace_relative_url_to_absolute(self, content):
        """Replace '../' leaded url with absolute uri.
        """
        p =  os.path.join(os.getcwd(), './src', '../')
        return content.replace('../', p)