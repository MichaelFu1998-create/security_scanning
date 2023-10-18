def voxspace_to_mmspace(img):
    """ Return a grid with coordinates in 3D physical space for `img`."""
    shape, affine = img.shape[:3], img.affine
    coords = np.array(np.meshgrid(*(range(i) for i in shape), indexing='ij'))
    coords = np.rollaxis(coords, 0, len(shape) + 1)
    mm_coords = nib.affines.apply_affine(affine, coords)

    return mm_coords