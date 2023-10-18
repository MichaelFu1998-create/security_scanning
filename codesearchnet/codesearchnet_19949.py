def summary(self):
        """
        A succinct summary of the Launcher configuration.  Unlike the
        repr, a summary does not have to be complete but must supply
        key information relevant to the user.
        """
        print("Type: %s" % self.__class__.__name__)
        print("Batch Name: %r" % self.batch_name)
        if self.tag:
            print("Tag: %s" % self.tag)
        print("Root directory: %r" % self.get_root_directory())
        print("Maximum concurrency: %s" % self.max_concurrency)
        if self.description:
            print("Description: %s" % self.description)