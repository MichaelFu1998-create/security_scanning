def get_root_directory(self, timestamp=None):
        """
        A helper method that supplies the root directory name given a
        timestamp.
        """
        if timestamp is None: timestamp = self.timestamp
        if self.timestamp_format is not None:
            root_name =  (time.strftime(self.timestamp_format, timestamp)
                          + '-' + self.batch_name)
        else:
            root_name = self.batch_name

        path = os.path.join(self.output_directory,
                                *(self.subdir+[root_name]))
        return os.path.abspath(path)