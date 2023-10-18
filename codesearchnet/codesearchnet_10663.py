def move_grid_to_radial_minimum(func):
    """ Checks whether any coordinates in the grid are radially near (0.0, 0.0), which can lead to numerical faults in \
    the evaluation of a light or mass profiles. If any coordinates are radially within the the radial minimum \
    threshold, their (y,x) coordinates are shifted to that value to ensure they are evaluated correctly.

    By default this radial minimum is not used, and users should be certain they use a value that does not impact \
    results.

    Parameters
    ----------
    func : (profile, *args, **kwargs) -> Object
        A function that takes a grid of coordinates which may have a singularity as (0.0, 0.0)

    Returns
    -------
        A function that can except cartesian or transformed coordinates
    """

    @wraps(func)
    def wrapper(profile, grid, *args, **kwargs):
        """

        Parameters
        ----------
        profile : SphericalProfile
            The profiles that owns the function
        grid : ndarray
            PlaneCoordinates in either cartesian or profiles coordinate system
        args
        kwargs

        Returns
        -------
            A value or coordinate in the same coordinate system as those passed in.
        """
        radial_minimum_config = conf.NamedConfig(f"{conf.instance.config_path}/radial_minimum.ini")
        grid_radial_minimum = radial_minimum_config.get("radial_minimum", profile.__class__.__name__, float)
        with np.errstate(all='ignore'):  # Division by zero fixed via isnan
            grid_radii = profile.grid_to_grid_radii(grid=grid)
            grid_radial_scale = np.where(grid_radii < grid_radial_minimum, grid_radial_minimum / grid_radii, 1.0)
            grid = np.multiply(grid, grid_radial_scale[:, None])
        grid[np.isnan(grid)] = grid_radial_minimum
        return func(profile, grid, *args, **kwargs)

    return wrapper