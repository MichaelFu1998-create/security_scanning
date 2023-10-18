def save_figures(image_path, fig_count, gallery_conf):
    """Save all open matplotlib figures of the example code-block

    Parameters
    ----------
    image_path : str
        Path where plots are saved (format string which accepts figure number)
    fig_count : int
        Previous figure number count. Figure number add from this number

    Returns
    -------
    list of strings containing the full path to each figure
    """
    figure_list = []

    fig_managers = matplotlib._pylab_helpers.Gcf.get_all_fig_managers()
    for fig_mngr in fig_managers:
        # Set the fig_num figure as the current figure as we can't
        # save a figure that's not the current figure.
        fig = plt.figure(fig_mngr.num)
        kwargs = {}
        to_rgba = matplotlib.colors.colorConverter.to_rgba
        for attr in ['facecolor', 'edgecolor']:
            fig_attr = getattr(fig, 'get_' + attr)()
            default_attr = matplotlib.rcParams['figure.' + attr]
            if to_rgba(fig_attr) != to_rgba(default_attr):
                kwargs[attr] = fig_attr

        current_fig = image_path.format(fig_count + fig_mngr.num)
        fig.savefig(current_fig, **kwargs)
        figure_list.append(current_fig)

    if gallery_conf.get('find_mayavi_figures', False):
        from mayavi import mlab
        e = mlab.get_engine()
        last_matplotlib_fig_num = len(figure_list)
        total_fig_num = last_matplotlib_fig_num + len(e.scenes)
        mayavi_fig_nums = range(last_matplotlib_fig_num, total_fig_num)

        for scene, mayavi_fig_num in zip(e.scenes, mayavi_fig_nums):
            current_fig = image_path.format(mayavi_fig_num)
            mlab.savefig(current_fig, figure=scene)
            # make sure the image is not too large
            scale_image(current_fig, current_fig, 850, 999)
            figure_list.append(current_fig)
        mlab.close(all=True)

    return figure_list