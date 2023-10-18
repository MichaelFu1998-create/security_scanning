def add_files(self, filelist, **kwargs):
        """Append files to file repository.
        
        ModificationMonitor can append files to repository using this.
        Please put the list of file names to `filelist` argument.

        :param filelist: the list of file nmaes
        """

        # check filelist is list type
        if not isinstance(filelist, list):
            raise TypeError("request the list type.")

        for file in filelist:
            self.add_file(file)