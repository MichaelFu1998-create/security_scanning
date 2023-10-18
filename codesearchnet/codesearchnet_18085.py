def set_model(self, mdl):
        """
        Setup the image model formation equation and corresponding objects into
        their various objects. `mdl` is a `peri.models.Model` object
        """
        self.mdl = mdl
        self.mdl.check_inputs(self.comps)

        for c in self.comps:
            setattr(self, '_comp_'+c.category, c)