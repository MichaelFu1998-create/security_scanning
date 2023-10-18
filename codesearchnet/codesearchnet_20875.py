def create_bodies(self):
        '''Create physics bodies corresponding to each marker in our data.'''
        self.bodies = {}
        for label in self.channels:
            body = self.world.create_body(
                'sphere', name='marker:{}'.format(label), radius=0.02)
            body.is_kinematic = True
            body.color = 0.9, 0.1, 0.1, 0.5
            self.bodies[label] = body