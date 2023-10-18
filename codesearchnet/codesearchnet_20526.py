def voxcoord_to_mm(cm, i, j, k):
    '''
    Parameters
    ----------
    cm: nipy.core.reference.coordinate_map.CoordinateMap

    i, j, k: floats
        Voxel coordinates

    Returns
    -------
    Triplet with real 3D world coordinates

    '''
    try:
        mm = cm([i, j, k])
    except Exception as exc:
        raise Exception('Error on converting coordinates.') from exc
    else:
        return mm