def update_from_model_change(self, oldmodel, newmodel, tile):
        """
        Update various internal variables from a model update from oldmodel to
        newmodel for the tile `tile`
        """
        self._loglikelihood -= self._calc_loglikelihood(oldmodel, tile=tile)
        self._loglikelihood += self._calc_loglikelihood(newmodel, tile=tile)
        self._residuals[tile.slicer] = self._data[tile.slicer] - newmodel