def plt_range(*args, **kwargs):
    """
    for i in plot_range(n):
        plt.imshow(imgs[i])

    left arrow yield prev value
    other key yield next value
    :param args:
    :return:
    """
    wait = kwargs.pop('wait', True)
    if not wait:
        # no interactive just pass range
        for i in progress(range(*args)):
            yield i
        return

    class _holder(object):
        pass
    hold = _holder()
    hold.i = 0
    hold.done = False

    def press(event):
        # import sys
        # sys.stdout.flush()
        hold.i += -1 if event.key == 'left' else 1
        hold.i = 0 if hold.i < 0 else hold.i

    def onclose(event):
        hold.done = True

    fig = kwargs.pop('fig', None)
    figsize = kwargs.pop('figsize', None)
    if fig is None:
        fig = plt.gcf()
        if figsize:
            fig.set_size_inches(figsize)
    elif isinstance(fig, (int, str)):
        if figsize:
            fig = plt.figure(fig, figsize=figsize)
        else:
            fig = plt.figure(fig)
    elif isinstance(fig, plt.Figure):
        if figsize:
            fig.set_size_inches(figsize)
    else:
        raise ValueError

    onkey_fig(press, fig)
    onclose_fig(onclose, fig)

    ranges = range(*args)
    l = len(ranges)

    while hold.i < l:
        print('hold.i', ranges[hold.i])
        yield ranges[hold.i]  # yield first without keypress
        before = hold.i
        while before == hold.i:
            while not fig.waitforbuttonpress(0.01):
                if hold.done:
                    return
            while fig.waitforbuttonpress(0.1):
                if hold.done:
                    return