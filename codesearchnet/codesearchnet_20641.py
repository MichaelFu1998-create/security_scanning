def all_childnodes_to_nifti1img(h5group):
    """Returns in a list all images found under h5group.

    Parameters
    ----------
    h5group: h5py.Group
        HDF group

    Returns
    -------
    list of nifti1Image
    """
    child_nodes = []
    def append_parent_if_dataset(name, obj):
        if isinstance(obj, h5py.Dataset):
            if name.split('/')[-1] == 'data':
                child_nodes.append(obj.parent)

    vols = []
    h5group.visititems(append_parent_if_dataset)
    for c in child_nodes:
        vols.append(hdfgroup_to_nifti1image(c))

    return vols