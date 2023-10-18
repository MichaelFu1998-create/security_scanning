def GNN_instance(x, idx=0, device=None, nh=20, **kwargs):
    """Run an instance of GNN, testing causal direction.

    :param m: data corresponding to the config : (N, 2) data, [:, 0] cause and [:, 1] effect
    :param pair_idx: print purposes
    :param run: numner of the run (for GPU dispatch)
    :param device: device on with the algorithm is going to be run on.
    :return:
    """
    device = SETTINGS.get_default(device=device)
    xy = scale(x).astype('float32')
    inputx = th.FloatTensor(xy[:, [0]]).to(device)
    target = th.FloatTensor(xy[:, [1]]).to(device)
    GNNXY = GNN_model(x.shape[0], device=device, nh=nh).to(device)
    GNNYX = GNN_model(x.shape[0], device=device, nh=nh).to(device)
    GNNXY.reset_parameters()
    GNNYX.reset_parameters()
    XY = GNNXY.run(inputx, target, **kwargs)
    YX = GNNYX.run(target, inputx, **kwargs)

    return [XY, YX]