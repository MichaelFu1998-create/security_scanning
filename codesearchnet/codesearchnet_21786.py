def remove(self):
        '''
        Remove this environment
        '''
        self.run_hook('preremove')
        utils.rmtree(self.path)
        self.run_hook('postremove')