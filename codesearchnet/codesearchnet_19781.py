def calc_centroids(self):
        """
        Identify the centroid positions for the target star at all epochs. Useful for verifying that there is
        no correlation between flux and position, as might be expected for high proper motion stars.
        """
        self.cm = np.zeros((len(self.postcard), 2))
        for i in range(len(self.postcard)):
            target = self.postcard[i]
            target[self.targets != 1] = 0.0
            self.cm[i] = center_of_mass(target)