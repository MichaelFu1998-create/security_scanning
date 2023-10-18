def frame(I=None, second=5, saveable=True, name='frame', cmap=None, fig_idx=12836):
    """Display a frame. Make sure OpenAI Gym render() is disable before using it.

    Parameters
    ----------
    I : numpy.array
        The image.
    second : int
        The display second(s) for the image(s), if saveable is False.
    saveable : boolean
        Save or plot the figure.
    name : str
        A name to save the image, if saveable is True.
    cmap : None or str
        'gray' for greyscale, None for default, etc.
    fig_idx : int
        matplotlib figure index.

    Examples
    --------
    >>> env = gym.make("Pong-v0")
    >>> observation = env.reset()
    >>> tl.visualize.frame(observation)

    """
    import matplotlib.pyplot as plt
    if saveable is False:
        plt.ion()
    plt.figure(fig_idx)  # show all feature images

    if len(I.shape) and I.shape[-1] == 1:  # (10,10,1) --> (10,10)
        I = I[:, :, 0]

    plt.imshow(I, cmap)
    plt.title(name)
    # plt.gca().xaxis.set_major_locator(plt.NullLocator())    # distable tick
    # plt.gca().yaxis.set_major_locator(plt.NullLocator())

    if saveable:
        plt.savefig(name + '.pdf', format='pdf')
    else:
        plt.draw()
        plt.pause(second)