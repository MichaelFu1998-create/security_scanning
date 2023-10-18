def update(self, params, values):
        """
        Actually perform an image (etc) update based on a set of params and
        values. These parameter can be any present in the components in any
        number. If there is only one component affected then difference image
        updates will be employed.
        """
        # FIXME needs to update priors
        comps = self.affected_components(params)

        if len(comps) == 0:
            return False

        # get the affected area of the model image
        otile, itile, iotile = self.get_update_io_tiles(params, values)

        if otile is None:
            return False

        # have all components update their tiles
        self.set_tile(otile)

        oldmodel = self._model[itile.slicer].copy()

        # here we diverge depending if there is only one component update
        # (so that we may calculate a variation / difference image) or if many
        # parameters are being update (should just update the whole model).
        if len(comps) == 1 and self.mdl.get_difference_model(comps[0].category):
            comp = comps[0]
            model0 = copy.deepcopy(comp.get())
            super(ImageState, self).update(params, values)
            model1 = copy.deepcopy(comp.get())

            diff = model1 - model0
            diff = self.mdl.evaluate(
                self.comps, 'get', diffmap={comp.category: diff}
            )

            if isinstance(model0, (float, int)):
                self._model[itile.slicer] += diff
            else:
                self._model[itile.slicer] += diff[iotile.slicer]
        else:
            super(ImageState, self).update(params, values)

            # allow the model to be evaluated using our components
            diff = self.mdl.evaluate(self.comps, 'get')
            self._model[itile.slicer] = diff[iotile.slicer]

        newmodel = self._model[itile.slicer].copy()

        # use the model image update to modify other class variables which
        # are hard to compute globally for small local updates
        self.update_from_model_change(oldmodel, newmodel, itile)
        return True