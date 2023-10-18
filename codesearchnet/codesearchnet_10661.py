def transform_grid(func):
    """Wrap the function in a function that checks whether the coordinates have been transformed. If they have not \ 
    been transformed then they are transformed.

    Parameters
    ----------
    func : (profiles, *args, **kwargs) -> Object
        A function that requires transformed coordinates

    Returns
    -------
        A function that can except cartesian or transformed coordinates
    """

    @wraps(func)
    def wrapper(profile, grid, *args, **kwargs):
        """

        Parameters
        ----------
        profile : GeometryProfile
            The profiles that owns the function
        grid : ndarray
            PlaneCoordinates in either cartesian or profiles coordinate system
        args
        kwargs

        Returns
        -------
            A value or coordinate in the same coordinate system as those passed in.
        """
        if not isinstance(grid, TransformedGrid):
            return func(profile, profile.transform_grid_to_reference_frame(grid), *args, **kwargs)
        else:
            return func(profile, grid, *args, **kwargs)

    return wrapper