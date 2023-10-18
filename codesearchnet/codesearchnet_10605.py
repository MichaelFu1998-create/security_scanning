def grid_at_redshift_from_image_plane_grid_and_redshift(self, image_plane_grid, redshift):
        """For an input grid of (y,x) arc-second image-plane coordinates, ray-trace the coordinates to any redshift in \
        the strong lens configuration.

        This is performed using multi-plane ray-tracing and the existing redshifts and planes of the tracer. However, \
        any redshift can be input even if a plane does not exist there, including redshifts before the first plane \
        of the lensing system.

        Parameters
        ----------
        image_plane_grid : ndsrray or grids.RegularGrid
            The image-plane grid which is traced to the redshift.
        redshift : float
            The redshift the image-plane grid is traced to.
        """

        # TODO : We need to come up with a better abstraction for multi-plane lensing 0_0

        image_plane_grid_stack = grids.GridStack(regular=image_plane_grid, sub=np.array([[0.0, 0.0]]),
                                                 blurring=np.array([[0.0, 0.0]]))

        tracer = TracerMultiPlanes(galaxies=self.galaxies, image_plane_grid_stack=image_plane_grid_stack,
                                   border=None, cosmology=self.cosmology)

        for plane_index in range(0, len(self.plane_redshifts)):

            new_grid_stack = image_plane_grid_stack

            if redshift <= tracer.plane_redshifts[plane_index]:

                # If redshift is between two planes, we need to map over all previous planes coordinates / deflections.

                if plane_index > 0:
                    for previous_plane_index in range(plane_index):
                        scaling_factor = cosmology_util.scaling_factor_between_redshifts_from_redshifts_and_cosmology(
                            redshift_0=tracer.plane_redshifts[previous_plane_index], redshift_1=redshift,
                            redshift_final=tracer.plane_redshifts[-1], cosmology=tracer.cosmology)

                        scaled_deflection_stack = lens_util.scaled_deflection_stack_from_plane_and_scaling_factor(
                            plane=tracer.planes[previous_plane_index], scaling_factor=scaling_factor)

                        new_grid_stack = \
                            lens_util.grid_stack_from_deflection_stack(grid_stack=new_grid_stack,
                                                                       deflection_stack=scaled_deflection_stack)

                # If redshift is before the first plane, no change to image pllane coordinates.

                elif plane_index == 0:

                    return new_grid_stack.regular

                return new_grid_stack.regular