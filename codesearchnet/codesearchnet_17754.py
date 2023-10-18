def fork(self,name):
        '''
        Create fork and store it in current instance
        '''
        fork=deepcopy(self)
        self[name]=fork
        return fork