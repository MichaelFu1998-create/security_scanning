def deepcopy(self):
        """
        Create a deep copy of the segmentation map object.

        Returns
        -------
        imgaug.SegmentationMapOnImage
            Deep copy.

        """
        segmap = SegmentationMapOnImage(self.arr, shape=self.shape, nb_classes=self.nb_classes)
        segmap.input_was = self.input_was
        return segmap