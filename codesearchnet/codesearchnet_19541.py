def movie_saving(outfile, showfun=imshow, fig=None, tight=True, drawopt=None, dpi=100, **movieopt):
    """
    contextmanager for PlotMovieWriter
    Example:

        with movie_saving('output.mp4', dpi=100) as plot:
            for i in range(10):
                plot(data[i])

    :param outfile:
    :param showfun:
    :param fig:
    :param tight:
    :param drawopt:
    :param dpi:
    :param movieopt: fps=5, codec=None, bitrate=None, extra_args=None, metadata=None
    :return:
    """
    if tight:
        plot_writer = ImageMovieWriter(outfile, showfun=showfun, fig=fig, drawopt=drawopt, dpi=dpi, **movieopt)
    else:
        plot_writer = PlotMovieWriter(outfile, showfun=showfun, fig=fig, drawopt=drawopt, dpi=dpi, **movieopt)

    try:
        yield plot_writer
    finally:
        plot_writer.finish()