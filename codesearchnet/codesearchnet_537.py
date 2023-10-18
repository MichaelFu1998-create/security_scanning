def npz_to_W_pdf(path=None, regx='w1pre_[0-9]+\.(npz)'):
    r"""Convert the first weight matrix of `.npz` file to `.pdf` by using `tl.visualize.W()`.

    Parameters
    ----------
    path : str
        A folder path to `npz` files.
    regx : str
        Regx for the file name.

    Examples
    ---------
    Convert the first weight matrix of w1_pre...npz file to w1_pre...pdf.

    >>> tl.files.npz_to_W_pdf(path='/Users/.../npz_file/', regx='w1pre_[0-9]+\.(npz)')

    """
    file_list = load_file_list(path=path, regx=regx)
    for f in file_list:
        W = load_npz(path, f)[0]
        logging.info("%s --> %s" % (f, f.split('.')[0] + '.pdf'))
        visualize.draw_weights(W, second=10, saveable=True, name=f.split('.')[0], fig_idx=2012)