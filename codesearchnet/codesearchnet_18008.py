def twoslice(field, center=None, size=6.0, cmap='bone_r', vmin=0, vmax=1,
        orientation='vertical', figpad=1.09, off=0.01):
    """
    Plot two parts of the ortho view, the two sections given by ``orientation``.
    """
    center = center or [i//2 for i in field.shape]
    slices = []
    for i,c in enumerate(center):
        blank = [np.s_[:]]*len(center)
        blank[i] = c
        slices.append(tuple(blank))

    z,y,x = [float(i) for i in field.shape]
    w = float(x + z)
    h = float(y + z)

    def show(field, ax, slicer, transpose=False):
        tmp = field[slicer] if not transpose else field[slicer].T
        ax.imshow(
            tmp, cmap=cmap, interpolation='nearest',
            vmin=vmin, vmax=vmax
        )
        ax.set_xticks([])
        ax.set_yticks([])
        ax.grid('off')

    if orientation.startswith('v'):
        # rect = l,b,w,h
        log.info('{} {} {} {} {} {}'.format(x, y, z, w, h, x/h))
        r = x/h
        q = y/h
        f = 1 / (1 + 3*off)
        fig = pl.figure(figsize=(size*r, size*f))
        ax1 = fig.add_axes((off, f*(1-q)+2*off, f, f*q))
        ax2 = fig.add_axes((off, off,           f, f*(1-q)))

        show(field, ax1, slices[0])
        show(field, ax2, slices[1])
    else:
        # rect = l,b,w,h
        r = y/w
        q = x/w
        f = 1 / (1 + 3*off)
        fig = pl.figure(figsize=(size*f, size*r))
        ax1 = fig.add_axes((off,    off,   f*q, f))
        ax2 = fig.add_axes((2*off+f*q, off, f*(1-q), f))

        show(field, ax1, slices[0])
        show(field, ax2, slices[2], transpose=True)

    return fig, ax1, ax2