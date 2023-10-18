def get_stats(self):
        """
        Get repository descriptive stats

        :Returns:
            #. numberOfDirectories (integer): Number of diretories in repository
            #. numberOfFiles (integer): Number of files in repository
        """
        if self.__path is None:
            return 0,0
        nfiles = 0
        ndirs  = 0
        for fdict in self.get_repository_state():
            fdname = list(fdict)[0]
            if fdname == '':
                continue
            if fdict[fdname].get('pyrepfileinfo', False):
                nfiles += 1
            elif fdict[fdname].get('pyrepdirinfo', False):
                ndirs += 1
            else:
                raise Exception('Not sure what to do next. Please report issue')
        return ndirs,nfiles