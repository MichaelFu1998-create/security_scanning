def _get_output(self, a, image):
        """ Looks up the precomputed adversarial image for a given image.

        """
        sd = np.square(self._input_images - image)
        mses = np.mean(sd, axis=tuple(range(1, sd.ndim)))
        index = np.argmin(mses)

        # if we run into numerical problems with this approach, we might
        # need to add a very tiny threshold here
        if mses[index] > 0:
            raise ValueError('No precomputed output image for this image')
        return self._output_images[index]