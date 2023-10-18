def indices_for_joint(self, name):
        '''Get a list of the indices for a specific joint.

        Parameters
        ----------
        name : str
            The name of the joint to look up.

        Returns
        -------
        list of int :
            A list of the index values for quantities related to the named
            joint. Often useful for getting, say, the angles for a specific
            joint in the skeleton.
        '''
        j = 0
        for joint in self.joints:
            if joint.name == name:
                return list(range(j, j + joint.ADOF))
            j += joint.ADOF
        return []