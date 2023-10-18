def scaled_deflection_stack_from_plane_and_scaling_factor(plane, scaling_factor):
    """Given a plane and scaling factor, compute a set of scaled deflections.

    Parameters
    -----------
    plane : plane.Plane
        The plane whose deflection stack is scaled.
    scaling_factor : float
        The factor the deflection angles are scaled by, which is typically the scaling factor between redshifts for \
        multi-plane lensing.
    """

    def scale(grid):
        return np.multiply(scaling_factor, grid)

    if plane.deflection_stack is not None:
        return plane.deflection_stack.apply_function(scale)
    else:
        return None