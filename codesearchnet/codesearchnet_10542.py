def plot_points(grid, points, pointcolor):
    """Plot a subset of points in a different color, to highlight a specifc region of the grid (e.g. how certain \
    pixels map between different planes).

    Parameters
    -----------
    grid : ndarray or data.array.grids.RegularGrid
        The (y,x) coordinates of the grid, in an array of shape (total_coordinates, 2).
    points : []
        A set of points that are plotted in a different colour for emphasis (e.g. to show the mappings between \
        different planes).
    pointcolor : str or None
        The color the points should be plotted. If None, the points are iterated through a cycle of colors.
    """
    if points is not None:

        if pointcolor is None:

            point_colors = itertools.cycle(["y", "r", "k", "g", "m"])
            for point_set in points:
                plt.scatter(y=np.asarray(grid[point_set, 0]),
                            x=np.asarray(grid[point_set, 1]), s=8, color=next(point_colors))

        else:

            for point_set in points:
                plt.scatter(y=np.asarray(grid[point_set, 0]),
                            x=np.asarray(grid[point_set, 1]), s=8, color=pointcolor)