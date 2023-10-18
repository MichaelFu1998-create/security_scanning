def mm_to_voxcoord(cm, x, y, z):
    '''
    Parameters
    ----------
    cm: nipy.core.reference.coordinate_map.CoordinateMap

    x, y, z: floats
        Physical coordinates

    Returns
    -------
    Triplet with 3D voxel coordinates
    '''
    try:
        vox = cm.inverse()([x, y, z])
    except Exception as exc:
        raise Exception('Error on converting coordinates') from exc
    else:
        return vox