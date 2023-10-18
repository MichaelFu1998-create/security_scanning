def sub_to_image_grid(func):
    """
    Wrap the function in a function that, if the grid is a sub-grid (grids.SubGrid), rebins the computed \
    values to the sub-grids corresponding regular-grid by taking the mean of each set of sub-gridded values.

    Parameters
    ----------
    func : (profiles, *args, **kwargs) -> Object
        A function that requires the sub-grid and galaxies.
    """

    @wraps(func)
    def wrapper(grid, galaxies, *args, **kwargs):
        """

        Parameters
        ----------
        grid : RegularGrid
            The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2).
        galaxies : [Galaxy]
            The list of galaxies a profile quantity (e.g. intensities) is computed for which is rebinned if it \
            is a sub-grid.

        Returns
        -------
        ndarray
            If a RegularGrid is input, the profile quantity of the galaxy (e.g. intensities) evaluated using this grid.

            If a SubGrid is input, the profile quantity of the galaxy (e.g. intensities) evaluated using the sub-grid \
            and rebinned to the regular-grids array dimensions.

        Examples
        ---------
        @grids.sub_to_image_grid
        def intensities_of_galaxies_from_grid(grid, galaxies):
            return sum(map(lambda g: g.intensities_from_grid(grid), galaxies))

        galaxy_util.intensities_of_galaxies_from_grid(grid=grid_stack.sub, galaxies=galaxies)
        """

        result = func(grid, galaxies, *args, *kwargs)

        if isinstance(grid, SubGrid):
            return grid.regular_data_1d_from_sub_data_1d(result)
        else:
            return result

    return wrapper