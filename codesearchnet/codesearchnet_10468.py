def compute_deflections_at_next_plane(plane_index, total_planes):
    """This function determines whether the tracer should compute the deflections at the next plane.

    This is True if there is another plane after this plane, else it is False..

    Parameters
    -----------
    plane_index : int
        The index of the plane we are deciding if we should compute its deflections.
    total_planes : int
        The total number of planes."""

    if plane_index < total_planes - 1:
        return True
    elif plane_index == total_planes - 1:
        return False
    else:
        raise exc.RayTracingException('A galaxy was not correctly allocated its previous / next redshifts')