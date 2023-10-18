def update(self, params, values):
        """
        Update the particles field given new parameter values
        """
        #1. Figure out if we're going to do a global update, in which
        #   case we just draw from scratch.
        global_update, particles = self._update_type(params)

        # if we are doing a global update, everything must change, so
        # starting fresh will be faster instead of add subtract
        if global_update:
            self.set_values(params, values)
            self.initialize()
            return

        # otherwise, update individual particles. delete the current versions
        # of the particles update the particles, and redraw them anew at the
        # places given by (params, values)
        oldargs = self._drawargs()
        for n in particles:
            self._draw_particle(self.pos[n], *listify(oldargs[n]), sign=-1)

        self.set_values(params, values)

        newargs = self._drawargs()
        for n in particles:
            self._draw_particle(self.pos[n], *listify(newargs[n]), sign=+1)