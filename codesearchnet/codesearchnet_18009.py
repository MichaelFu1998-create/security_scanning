def circles(st, layer, axis, ax=None, talpha=1.0, cedge='white', cface='white'):
    """
    Plots a set of circles corresponding to a slice through the platonic
    structure. Copied from twoslice_overlay with comments, standaloneness.

    Inputs
    ------
        pos : array of particle positions; [N,3]
        rad : array of particle radii; [N]
        ax : plt.axis instance
        layer : Which layer of the slice to use.
        axis : The slice of the image, 0, 1, or 2.
        cedge : edge color
        cface : face color
        talpha : Alpha of the thing
    """
    pos = st.obj_get_positions()
    rad = st.obj_get_radii()
    shape = st.ishape.shape.tolist()
    shape.pop(axis) #shape is now the shape of the image
    if ax is None:
        fig = plt.figure()
        axisbg = 'white' if cface == 'black' else 'black'
        sx, sy = ((1,shape[1]/float(shape[0])) if shape[0] > shape[1] else
                (shape[0]/float(shape[1]), 1))
        ax = fig.add_axes((0,0, sx, sy), axisbg=axisbg)
    # get the index of the particles we want to include
    particles = np.arange(len(pos))[np.abs(pos[:,axis] - layer) < rad]

    # for each of these particles display the effective radius
    # in the proper place
    scale = 1.0 #np.max(shape).astype('float')
    for i in particles:
        p = pos[i].copy()
        r = 2*np.sqrt(rad[i]**2 - (p[axis] - layer)**2)
        #CIRCLE IS IN FIGURE COORDINATES!!!
        if axis==0:
            ix = 1; iy = 2
        elif axis == 1:
            ix = 0; iy = 2
        elif axis==2:
            ix = 0; iy = 1
        c = Circle((p[ix]/scale, p[iy]/scale), radius=r/2/scale, fc=cface,
                ec=cedge, alpha=talpha)
        ax.add_patch(c)
    # plt.axis([0,1,0,1])
    plt.axis('equal') #circles not ellipses
    return ax