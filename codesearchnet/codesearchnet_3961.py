def graph_evaluation(data, adj_matrix, gpu=None, gpu_id=0, **kwargs):
    """Evaluate a graph taking account of the hardware."""
    gpu = SETTINGS.get_default(gpu=gpu)
    device = 'cuda:{}'.format(gpu_id) if gpu else 'cpu'
    obs = th.FloatTensor(data).to(device)
    cgnn = CGNN_model(adj_matrix, data.shape[0], gpu_id=gpu_id, **kwargs).to(device)
    cgnn.reset_parameters()
    return cgnn.run(obs, **kwargs)