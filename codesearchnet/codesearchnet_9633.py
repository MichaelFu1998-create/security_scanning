def memory_file(data=None, profile=None):
    """
    Return a rasterio.io.MemoryFile instance from input.

    Parameters
    ----------
    data : array
        array to be written
    profile : dict
        rasterio profile for MemoryFile
    """
    memfile = MemoryFile()
    profile.update(width=data.shape[-2], height=data.shape[-1])
    with memfile.open(**profile) as dataset:
        dataset.write(data)
    return memfile