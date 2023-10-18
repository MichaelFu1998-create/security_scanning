def load_image(self):
        """ Read the file and perform any transforms to get a loaded image """
        try:
            image = initializers.load_tiff(self.filename)
            image = initializers.normalize(
                image, invert=self.invert, scale=self.exposure,
                dtype=self.float_precision
            )
        except IOError as e:
            log.error("Could not find image '%s'" % self.filename)
            raise e

        return image