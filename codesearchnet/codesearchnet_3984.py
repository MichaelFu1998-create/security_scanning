def run_SAM(df_data, skeleton=None, **kwargs):
    """Execute the SAM model.

    :param df_data: Input data; either np.array or pd.DataFrame
    """
    gpu = kwargs.get('gpu', False)
    gpu_no = kwargs.get('gpu_no', 0)

    train_epochs = kwargs.get('train_epochs', 1000)
    test_epochs = kwargs.get('test_epochs', 1000)
    batch_size = kwargs.get('batch_size', -1)

    lr_gen = kwargs.get('lr_gen', 0.1)
    lr_disc = kwargs.get('lr_disc', lr_gen)
    verbose = kwargs.get('verbose', True)
    regul_param = kwargs.get('regul_param', 0.1)
    dnh = kwargs.get('dnh', None)
    plot = kwargs.get("plot", False)
    plot_generated_pair = kwargs.get("plot_generated_pair", False)

    d_str = "Epoch: {} -- Disc: {} -- Gen: {} -- L1: {}"
    try:
        list_nodes = list(df_data.columns)
        df_data = (df_data[list_nodes]).values
    except AttributeError:
        list_nodes = list(range(df_data.shape[1]))
    data = df_data.astype('float32')
    data = th.from_numpy(data)
    if batch_size == -1:
        batch_size = data.shape[0]
    rows, cols = data.size()

    # Get the list of indexes to ignore
    if skeleton is not None:
        zero_components = [[] for i in range(cols)]
        skel = nx.adj_matrix(skeleton, weight=None)
        for i, j in zip(*((1-skel).nonzero())):
            zero_components[j].append(i)
    else:
        zero_components = [[i] for i in range(cols)]
    sam = SAM_generators((rows, cols), zero_components, batch_norm=True, **kwargs)

    # Begin UGLY
    activation_function = kwargs.get('activation_function', th.nn.Tanh)
    try:
        del kwargs["activation_function"]
    except KeyError:
        pass
    discriminator_sam = SAM_discriminator(
        [cols, dnh, dnh, 1], batch_norm=True,
        activation_function=th.nn.LeakyReLU,
        activation_argument=0.2, **kwargs)
    kwargs["activation_function"] = activation_function
    # End of UGLY

    if gpu:
        sam = sam.cuda(gpu_no)
        discriminator_sam = discriminator_sam.cuda(gpu_no)
        data = data.cuda(gpu_no)

    # Select parameters to optimize : ignore the non connected nodes
    criterion = th.nn.BCEWithLogitsLoss()
    g_optimizer = th.optim.Adam(sam.parameters(), lr=lr_gen)
    d_optimizer = th.optim.Adam(
        discriminator_sam.parameters(), lr=lr_disc)

    true_variable = Variable(
        th.ones(batch_size, 1), requires_grad=False)
    false_variable = Variable(
        th.zeros(batch_size, 1), requires_grad=False)
    causal_filters = th.zeros(data.shape[1], data.shape[1])

    if gpu:
        true_variable = true_variable.cuda(gpu_no)
        false_variable = false_variable.cuda(gpu_no)
        causal_filters = causal_filters.cuda(gpu_no)

    data_iterator = DataLoader(data, batch_size=batch_size, shuffle=True)

    # TRAIN
    for epoch in range(train_epochs + test_epochs):
        for i_batch, batch in enumerate(data_iterator):
            batch = Variable(batch)
            batch_vectors = [batch[:, [i]] for i in range(cols)]

            g_optimizer.zero_grad()
            d_optimizer.zero_grad()

            # Train the discriminator
            generated_variables = sam(batch)
            disc_losses = []
            gen_losses = []

            for i in range(cols):
                generator_output = th.cat([v for c in [batch_vectors[: i], [
                    generated_variables[i]],
                    batch_vectors[i + 1:]] for v in c], 1)
                # 1. Train discriminator on fake
                disc_output_detached = discriminator_sam(
                    generator_output.detach())
                disc_output = discriminator_sam(generator_output)
                disc_losses.append(
                    criterion(disc_output_detached, false_variable))

                # 2. Train the generator :
                gen_losses.append(criterion(disc_output, true_variable))

            true_output = discriminator_sam(batch)
            adv_loss = sum(disc_losses)/cols + \
                criterion(true_output, true_variable)
            gen_loss = sum(gen_losses)

            adv_loss.backward()
            d_optimizer.step()

            # 3. Compute filter regularization
            filters = th.stack(
                [i.fs_filter[0, :-1].abs() for i in sam.blocks], 1)
            l1_reg = regul_param * filters.sum()
            loss = gen_loss + l1_reg

            if verbose and epoch % 200 == 0 and i_batch == 0:

                print(str(i) + " " + d_str.format(epoch,
                                                  adv_loss.item(),
                                                  gen_loss.item() / cols,
                                                  l1_reg.item()))
            loss.backward()

            # STORE ASSYMETRY values for output
            if epoch > train_epochs:
                causal_filters.add_(filters.data)
            g_optimizer.step()

            if plot:
                plot_curves(i_batch, adv_loss, gen_loss, l1_reg, cols)

            if plot_generated_pair and epoch % 200 == 0:
                plot_gen(epoch, batch, generated_variables)

    return causal_filters.div_(test_epochs).cpu().numpy()