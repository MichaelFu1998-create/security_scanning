def compress(self, delete_tif=False, folder=None):
        """Lossless compress all images in experiment to PNG. If folder is
        omitted, images will not be moved.

        Images which already exists in PNG are omitted.

        Parameters
        ----------
        folder : string
            Where to store PNGs. Defaults to the folder they are in.
        delete_tif : bool
            If set to truthy value, ome.tifs will be deleted after compression.

        Returns
        -------
        list
            Filenames of PNG images. Files which already exists before
            compression are also returned.
        """
        return compress(self.images, delete_tif, folder)