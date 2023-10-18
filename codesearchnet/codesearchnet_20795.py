def state(self):
        '''The state of this body includes:

            - name of the body (str)
            - position (3-tuple)
            - quaternion (4-tuple)
            - linear velocity (3-tuple)
            - angular velocity (3-tuple)
        '''
        return BodyState(self.name,
                         tuple(self.position),
                         tuple(self.quaternion),
                         tuple(self.linear_velocity),
                         tuple(self.angular_velocity))