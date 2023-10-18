def doplot(image0, image1, xs, crbs, errors, labels, diff_image_scale=0.1,
        dolabels=True, multiple_crbs=True, xlim=None, ylim=None, highlight=None,
        detailed_labels=False, xlabel="", title=""):
    """
    Standardizing the plot format of the does_matter section.  See any of the
    accompaning files to see how to use this generalized plot.

    image0 : ground true
    image1 : difference image
    xs : list of x values for the plots
    crbs : list of lines of values of the crbs
    errors : list of lines of errors
    labels : legend labels for each curve
    """
    if len(crbs) != len(errors) or len(crbs) != len(labels):
        raise IndexError, "lengths are not consistent"

    fig = pl.figure(figsize=(14,7))

    ax = fig.add_axes([0.43, 0.15, 0.52, 0.75])
    gs = ImageGrid(fig, rect=[0.05, 0.05, 0.25, 0.90], nrows_ncols=(2,1), axes_pad=0.25,
            cbar_location='right', cbar_mode='each', cbar_size='10%', cbar_pad=0.04)

    diffm = diff_image_scale*np.ceil(np.abs(image1).max()/diff_image_scale)

    im0 = gs[0].imshow(image0, vmin=0, vmax=1, cmap='bone_r')
    im1 = gs[1].imshow(image1, vmin=-diffm, vmax=diffm, cmap='RdBu')
    cb0 = pl.colorbar(im0, cax=gs[0].cax, ticks=[0,1])
    cb1 = pl.colorbar(im1, cax=gs[1].cax, ticks=[-diffm,diffm]) 
    cb0.ax.set_yticklabels(['0', '1'])
    cb1.ax.set_yticklabels(['-%0.1f' % diffm, '%0.1f' % diffm])
    image_names = ["Reference", "Difference"]

    for i in xrange(2):
        gs[i].set_xticks([])
        gs[i].set_yticks([])
        gs[i].set_ylabel(image_names[i])

        if dolabels:
            lbl(gs[i], figlbl[i])

    symbols = ['o', '^', 'D', '>']
    for i in xrange(len(labels)):
        c = COLORS[i]

        if multiple_crbs or i == 0:
            if multiple_crbs:
                label = labels[i] if (i != 0 and not detailed_labels) else '%s CRB' % labels[i]
            else:
                label = 'CRB'
            ax.plot(xs[i], crbs[i], '-', c=c, lw=3, label=label)

        label = labels[i] if (i != 0 and not detailed_labels) else '%s Error' % labels[i]
        ax.plot(xs[i], errors[i], symbols[i], ls='--', lw=2, c=c, label=label, ms=12)

    if dolabels:
        lbl(ax, 'D')
    ax.loglog()
    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    ax.legend(loc='upper left', ncol=2, prop={'size': 18}, numpoints=1)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(r"Position CRB, Error")
    ax.grid(False, which='both', axis='both')
    ax.set_title(title)

    return gs, ax