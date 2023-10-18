def add_torques(self, torques):
        '''Add torques for each degree of freedom in the skeleton.

        Parameters
        ----------
        torques : list of float
            A list of the torques to add to each degree of freedom in the
            skeleton.
        '''
        j = 0
        for joint in self.joints:
            joint.add_torques(
                list(torques[j:j+joint.ADOF]) + [0] * (3 - joint.ADOF))
            j += joint.ADOF