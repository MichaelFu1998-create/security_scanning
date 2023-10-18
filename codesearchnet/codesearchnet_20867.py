def joint_distances(self):
        '''Get the current joint separations for the skeleton.

        Returns
        -------
        distances : list of float
            A list expressing the distance between the two joint anchor points,
            for each joint in the skeleton. These quantities describe how
            "exploded" the bodies in the skeleton are; a value of 0 indicates
            that the constraints are perfectly satisfied for that joint.
        '''
        return [((np.array(j.anchor) - j.anchor2) ** 2).sum() for j in self.joints]