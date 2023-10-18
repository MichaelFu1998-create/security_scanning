def save(self, filename, imdata, **data):
        """
        Data may be either a PIL Image object or a Numpy array.
        """
        if isinstance(imdata, numpy.ndarray):
            imdata = Image.fromarray(numpy.uint8(imdata))
        elif isinstance(imdata, Image.Image):
            imdata.save(self._savepath(filename))