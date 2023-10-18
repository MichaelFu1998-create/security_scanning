def replies(self):
        """ returns a list of strings """
        fs_reply_path = join(self.fs_replies_path, 'message_001.txt')
        if exists(fs_reply_path):
            return [load(open(fs_reply_path, 'r'))]
        else:
            return []