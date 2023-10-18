def message(self):
        """ returns the user submitted text
        """
        try:
            with open(join(self.fs_path, u'message')) as message_file:
                return u''.join([line.decode('utf-8') for line in message_file.readlines()])
        except IOError:
            return u''