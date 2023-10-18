def CNN2d(CNN=None, second=10, saveable=True, name='cnn', fig_idx=3119362):
    """Display a group of RGB or Greyscale CNN masks.

    Parameters
    ----------
    CNN : numpy.array
        The image. e.g: 64 5x5 RGB images can be (5, 5, 3, 64).
    second : int
        The display second(s) for the image(s), if saveable is False.
    saveable : boolean
        Save or plot the figure.
    name : str
        A name to save the image, if saveable is True.
    fig_idx : int
        The matplotlib figure index.

    Examples
    --------
    >>> tl.visualize.CNN2d(network.all_params[0].eval(), second=10, saveable=True, name='cnn1_mnist', fig_idx=2012)

    """
    import matplotlib.pyplot as plt
    # tl.logging.info(CNN.shape)    # (5, 5, 3, 64)
    # exit()
    n_mask = CNN.shape[3]
    n_row = CNN.shape[0]
    n_col = CNN.shape[1]
    n_color = CNN.shape[2]
    row = int(np.sqrt(n_mask))
    col = int(np.ceil(n_mask / row))
    plt.ion()  # active mode
    fig = plt.figure(fig_idx)
    count = 1
    for _ir in range(1, row + 1):
        for _ic in range(1, col + 1):
            if count > n_mask:
                break
            fig.add_subplot(col, row, count)
            # tl.logging.info(CNN[:,:,:,count-1].shape, n_row, n_col)   # (5, 1, 32) 5 5
            # exit()
            # plt.imshow(
            #         np.reshape(CNN[count-1,:,:,:], (n_row, n_col)),
            #         cmap='gray', interpolation="nearest")     # theano
            if n_color == 1:
                plt.imshow(np.reshape(CNN[:, :, :, count - 1], (n_row, n_col)), cmap='gray', interpolation="nearest")
            elif n_color == 3:
                plt.imshow(
                    np.reshape(CNN[:, :, :, count - 1], (n_row, n_col, n_color)), cmap='gray', interpolation="nearest"
                )
            else:
                raise Exception("Unknown n_color")
            plt.gca().xaxis.set_major_locator(plt.NullLocator())  # distable tick
            plt.gca().yaxis.set_major_locator(plt.NullLocator())
            count = count + 1
    if saveable:
        plt.savefig(name + '.pdf', format='pdf')
    else:
        plt.draw()
        plt.pause(second)