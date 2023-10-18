def ls(self, glob_str):
        """
        Return just the filenames that match `glob_str` inside the store directory.

        :param str glob_str: A glob string, i.e. 'state_*'
        :return: list of matched keys
        """
        path = os.path.join(self.uri, glob_str)
        return [os.path.split(s)[1] for s in glob.glob(path)]