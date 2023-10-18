def _build_indices(X, flann_args):
    "Builds FLANN indices for each bag."
    # TODO: should probably multithread this
    logger.info("Building indices...")
    indices = [None] * len(X)
    for i, bag in enumerate(plog(X, name="index building")):
        indices[i] = idx = FLANNIndex(**flann_args)
        idx.build_index(bag)
    return indices