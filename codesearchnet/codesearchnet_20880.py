def forces(self, dx_tm1=None):
        '''Return an array of the forces exerted by marker springs.

        Notes
        -----

        The forces exerted by the marker springs can be approximated by::

          F = kp * dx

        where ``dx`` is the current array of marker distances. An even more
        accurate value is computed by approximating the velocity of the spring
        displacement::

          F = kp * dx + kd * (dx - dx_tm1) / dt

        where ``dx_tm1`` is an array of distances from the previous time step.

        Parameters
        ----------
        dx_tm1 : ndarray
            An array of distances from markers to their attachment targets,
            measured at the previous time step.

        Returns
        -------
        F : ndarray
            An array of forces that the markers are exerting on the skeleton.
        '''
        cfm = self.cfms[self._frame_no][:, None]
        kp = self.erp / (cfm * self.world.dt)
        kd = (1 - self.erp) / cfm
        dx = self.distances()
        F = kp * dx
        if dx_tm1 is not None:
            bad = np.isnan(dx) | np.isnan(dx_tm1)
            F[~bad] += (kd * (dx - dx_tm1) / self.world.dt)[~bad]
        return F