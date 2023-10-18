def relocated_grid_from_grid_jit(grid, border_grid):
        """ Relocate the coordinates of a grid to its border if they are outside the border. This is performed as \
        follows:

        1) Use the mean value of the grid's y and x coordinates to determine the origin of the grid.
        2) Compute the radial distance of every grid coordinate from the origin.
        3) For every coordinate, find its nearest pixel in the border.
        4) Determine if it is outside the border, by comparing its radial distance from the origin to its paid \
           border pixel's radial distance.
        5) If its radial distance is larger, use the ratio of radial distances to move the coordinate to the border \
           (if its inside the border, do nothing).
        """
        border_origin = np.zeros(2)
        border_origin[0] = np.mean(border_grid[:, 0])
        border_origin[1] = np.mean(border_grid[:, 1])
        border_grid_radii = np.sqrt(np.add(np.square(np.subtract(border_grid[:, 0], border_origin[0])),
                                           np.square(np.subtract(border_grid[:, 1], border_origin[1]))))
        border_min_radii = np.min(border_grid_radii)

        grid_radii = np.sqrt(np.add(np.square(np.subtract(grid[:, 0], border_origin[0])),
                                    np.square(np.subtract(grid[:, 1], border_origin[1]))))

        for pixel_index in range(grid.shape[0]):

            if grid_radii[pixel_index] > border_min_radii:

                closest_pixel_index = np.argmin(np.square(grid[pixel_index, 0] - border_grid[:, 0]) +
                                                np.square(grid[pixel_index, 1] - border_grid[:, 1]))

                move_factor = border_grid_radii[closest_pixel_index] / grid_radii[pixel_index]
                if move_factor < 1.0:
                    grid[pixel_index, :] = move_factor * (grid[pixel_index, :] - border_origin[:]) + border_origin[:]

        return grid