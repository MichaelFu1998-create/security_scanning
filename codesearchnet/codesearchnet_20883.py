def step(self, substeps=2):
        '''Advance the physics world by one step.

        Typically this is called as part of a :class:`pagoda.viewer.Viewer`, but
        it can also be called manually (or some other stepping mechanism
        entirely can be used).
        '''
        # by default we step by following our loaded marker data.
        self.frame_no += 1
        try:
            next(self.follower)
        except (AttributeError, StopIteration) as err:
            self.reset()