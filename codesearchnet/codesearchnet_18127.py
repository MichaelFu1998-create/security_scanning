def _pick_state_im_name(state_name, im_name, use_full_path=False):
    """
    If state_name or im_name is None, picks them interactively through Tk,
    and then sets with or without the full path.

    Parameters
    ----------
        state_name : {string, None}
            The name of the state. If None, selected through Tk.
        im_name : {string, None}
            The name of the image. If None, selected through Tk.
        use_full_path : Bool, optional
            Set to True to return the names as full paths rather than
            relative paths. Default is False (relative path).
    """
    initial_dir = os.getcwd()
    if (state_name is None) or (im_name is None):
        wid = tk.Tk()
        wid.withdraw()
    if state_name is None:
        state_name = tkfd.askopenfilename(
                initialdir=initial_dir, title='Select pre-featured state')
        os.chdir(os.path.dirname(state_name))

    if im_name is None:
        im_name = tkfd.askopenfilename(
                initialdir=initial_dir, title='Select new image')

    if (not use_full_path) and (os.path.dirname(im_name) != ''):
        im_path = os.path.dirname(im_name)
        os.chdir(im_path)
        im_name = os.path.basename(im_name)
    else:
        os.chdir(initial_dir)
    return state_name, im_name