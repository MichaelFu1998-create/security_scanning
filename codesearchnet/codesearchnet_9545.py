def raw_conf_process_pyramid(raw_conf):
    """
    Loads the process pyramid of a raw configuration.

    Parameters
    ----------
    raw_conf : dict
        Raw mapchete configuration as dictionary.

    Returns
    -------
    BufferedTilePyramid
    """
    return BufferedTilePyramid(
        raw_conf["pyramid"]["grid"],
        metatiling=raw_conf["pyramid"].get("metatiling", 1),
        pixelbuffer=raw_conf["pyramid"].get("pixelbuffer", 0)
    )