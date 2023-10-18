def images(self):
        "List of paths to images."
        tifs = _pattern(self._image_path, extension='tif')
        pngs = _pattern(self._image_path, extension='png')
        imgs = []
        imgs.extend(glob(tifs))
        imgs.extend(glob(pngs))
        return imgs