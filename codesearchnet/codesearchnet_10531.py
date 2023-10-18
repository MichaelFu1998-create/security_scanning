def setup_image_plane_pixelization_grid_from_galaxies_and_grid_stack(galaxies, grid_stack):
    """An image-plane pixelization is one where its pixel centres are computed by tracing a sparse grid of pixels from \
    the image's regular grid to other planes (e.g. the source-plane).

    Provided a galaxy has an image-plane pixelization, this function returns a new *GridStack* instance where the \
    image-plane pixelization's sparse grid is added to it as an attibute.

    Thus, when the *GridStack* are are passed to the *ray_tracing* module this sparse grid is also traced and the \
    traced coordinates represent the centre of each pixelization pixel.

    Parameters
    -----------
    galaxies : [model.galaxy.galaxy.Galaxy]
        A list of galaxies, which may contain pixelizations and an *ImagePlanePixelization*.
    grid_stacks : image.array.grid_stacks.GridStack
        The collection of grid_stacks (regular, sub, etc.) which the image-plane pixelization grid (referred to as pix) \
        may be added to.
    """
    if not isinstance(grid_stack.regular, grids.PaddedRegularGrid):
        for galaxy in galaxies:
            if hasattr(galaxy, 'pixelization'):
                if isinstance(galaxy.pixelization, ImagePlanePixelization):

                    image_plane_pix_grid = galaxy.pixelization.image_plane_pix_grid_from_regular_grid(
                        regular_grid=grid_stack.regular)
                    return grid_stack.new_grid_stack_with_pix_grid_added(pix_grid=image_plane_pix_grid.sparse_grid,
                                                                         regular_to_nearest_pix=image_plane_pix_grid.regular_to_sparse)

    return grid_stack