def distances(self):
        '''Get a list of the distances between markers and their attachments.

        Returns
        -------
        distances : ndarray of shape (num-markers, 3)
            Array of distances for each marker joint in our attachment setup. If
            a marker does not currently have an associated joint (e.g. because
            it is not currently visible) this will contain NaN for that row.
        '''
        distances = []
        for label in self.labels:
            joint = self.joints.get(label)
            distances.append([np.nan, np.nan, np.nan] if joint is None else
                             np.array(joint.getAnchor()) - joint.getAnchor2())
        return np.array(distances)