def deepcopy(self):
        """
        Create a deep copy of the Heatmaps object.

        Returns
        -------
        imgaug.HeatmapsOnImage
            Deep copy.

        """
        return HeatmapsOnImage(self.get_arr(), shape=self.shape, min_value=self.min_value, max_value=self.max_value)