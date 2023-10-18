def load_repository(self, path, verbose=True, ntrials=3):
        """
        Load repository from a directory path and update the current instance.
        First, new repository still will be loaded. If failed, then old
        style repository load will be tried.

        :Parameters:
            #. path (string): The path of the directory from where to load
               the repository from. If '.' or an empty string is passed,
               the current working directory will be used.
            #. verbose (boolean): Whether to be verbose about abnormalities
            #. ntrials (int): After aquiring all locks, ntrials is the maximum
               number of trials allowed before failing.
               In rare cases, when multiple processes
               are accessing the same repository components, different processes
               can alter repository components between successive lock releases
               of some other process. Bigger number of trials lowers the
               likelyhood of failure due to multiple processes same time
               alteration.

        :Returns:
             #. repository (pyrep.Repository): returns self repository with loaded data.
        """
        assert isinstance(ntrials, int), "ntrials must be integer"
        assert ntrials>0, "ntrials must be >0"
        repo = None
        for _trial in range(ntrials):
            try:
                self.__load_repository(path=path, verbose=True)
            except Exception as err1:
                try:
                    from .OldRepository import Repository
                    REP = Repository(path)
                except Exception as err2:
                    #traceback.print_exc()
                    error = "Unable to load repository using neiher new style (%s) nor old style (%s)"%(err1, err2)
                    if self.DEBUG_PRINT_FAILED_TRIALS: print("Trial %i failed in Repository.%s (%s). Set Repository.DEBUG_PRINT_FAILED_TRIALS to False to mute"%(_trial, inspect.stack()[1][3], str(error)))
                else:
                    error = None
                    repo  = REP
                    break
            else:
                error = None
                repo  = self
                break
        # check and return
        assert error is None, error
        return repo