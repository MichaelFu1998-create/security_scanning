def update(self, containers):
        '''Update the current state file with the specified contents'''
        self._containers = deepcopy(containers)
        self.__write(containers, initialize=False)