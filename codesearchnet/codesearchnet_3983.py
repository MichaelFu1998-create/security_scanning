def plot_gen(epoch, batch, generated_variables, pairs_to_plot=[[0, 1]]):
    """Plot generated pairs of variables."""
    from matplotlib import pyplot as plt
    if epoch == 0:
        plt.ion()
    plt.clf()
    for (i, j) in pairs_to_plot:

        plt.scatter(generated_variables[i].data.cpu().numpy(
        ), batch.data.cpu().numpy()[:, j], label="Y -> X")
        plt.scatter(batch.data.cpu().numpy()[
            :, i], generated_variables[j].data.cpu().numpy(), label="X -> Y")

        plt.scatter(batch.data.cpu().numpy()[:, i], batch.data.cpu().numpy()[
            :, j], label="original data")
        plt.legend()

    plt.pause(0.01)