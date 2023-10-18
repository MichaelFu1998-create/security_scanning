def plot_pause(timeout=None, msg=''):
    """
    todo : add some example
    :param timeout: wait time. if None, blocking
    :param msg:
    :return:
    """

    if timeout is not None:
        print(msg or 'Press key for continue in time {}'.format(timeout))
        plt.waitforbuttonpress(timeout=timeout)
        return True

    print(msg or 'Press key for continue')
    while not plt.waitforbuttonpress(timeout=0.01):
        if not plt.get_fignums():
            return False
    return len(plt.get_fignums()) != 0