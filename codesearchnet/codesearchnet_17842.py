def guess_invert(st):
    """Guesses whether particles are bright on a dark bkg or vice-versa

    Works by checking whether the intensity at the particle centers is
    brighter or darker than the average intensity of the image, by
    comparing the median intensities of each.

    Parameters
    ----------
    st : :class:`peri.states.ImageState`

    Returns
    -------
    invert : bool
        Whether to invert the image for featuring.
    """
    pos = st.obj_get_positions()
    pxinds_ar = np.round(pos).astype('int')
    inim = st.ishape.translate(-st.pad).contains(pxinds_ar)
    pxinds_tuple = tuple(pxinds_ar[inim].T)
    pxvals = st.data[pxinds_tuple]
    invert = np.median(pxvals) < np.median(st.data)  # invert if dark particles
    return invert