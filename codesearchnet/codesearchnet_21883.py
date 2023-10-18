def validate(self):
        '''Validate all the entries in the environment cache.'''

        for env in list(self):
            if not env.exists:
                self.remove(env)