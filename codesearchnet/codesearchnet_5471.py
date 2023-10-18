def initialize(self, containers):
        '''
        Initialize a new state file with the given contents.
        This function fails in case the state file already exists.
        '''
        self._containers = deepcopy(containers)
        self.__write(containers, initialize=True)