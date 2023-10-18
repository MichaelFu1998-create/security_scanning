def log_file(self, url=None):
        """
        Write to a local log file
        """
        if url is None:
            url = self.url
        f = re.sub("file://", "", url)
        try:
            with open(f, "a") as of:
                of.write(str(self.store.get_json_tuples(True)))
        except IOError as e:
            print(e)
            print("Could not write the content to the file..")