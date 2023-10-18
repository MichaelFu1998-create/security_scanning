def _key(cls, obs):
        '''Provides sorting index for Observation objects'''
        if not isinstance(obs, Observation):
            raise JamsError('{} must be of type jams.Observation'.format(obs))

        return obs.time