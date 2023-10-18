def generative_model(s,x,y,z,r, factor=1.1):
    """
    Samples x,y,z,r are created by:
    b = s.blocks_particle(#)
    h = runner.sample_state(s, b, stepout=0.05, N=2000, doprint=True)
    z,y,x,r = h.get_histogram().T
    """
    pl.close('all')

    slicez = int(round(z.mean()))
    slicex = s.image.shape[2]//2
    slicer1 = np.s_[slicez,s.pad:-s.pad,s.pad:-s.pad]
    slicer2 = np.s_[s.pad:-s.pad,s.pad:-s.pad,slicex]
    center = (slicez, s.image.shape[1]//2, slicex)

    fig = pl.figure(figsize=(factor*13,factor*10))

    #=========================================================================
    #=========================================================================
    gs1 = ImageGrid(fig, rect=[0.0, 0.6, 1.0, 0.35], nrows_ncols=(1,3),
            axes_pad=0.1)
    ax_real = gs1[0]
    ax_fake = gs1[1]
    ax_diff = gs1[2]

    diff = s.get_model_image() - s.image
    ax_real.imshow(s.image[slicer1], cmap=pl.cm.bone_r)
    ax_real.set_xticks([])
    ax_real.set_yticks([])
    ax_real.set_title("Confocal image", fontsize=24)
    ax_fake.imshow(s.get_model_image()[slicer1], cmap=pl.cm.bone_r)
    ax_fake.set_xticks([])
    ax_fake.set_yticks([])
    ax_fake.set_title("Model image", fontsize=24)
    ax_diff.imshow(diff[slicer1], cmap=pl.cm.RdBu, vmin=-0.1, vmax=0.1)
    ax_diff.set_xticks([])
    ax_diff.set_yticks([])
    ax_diff.set_title("Difference", fontsize=24)

    #=========================================================================
    #=========================================================================
    gs2 = ImageGrid(fig, rect=[0.1, 0.0, 0.4, 0.55], nrows_ncols=(3,2),
            axes_pad=0.1)
    ax_plt1 = fig.add_subplot(gs2[0])
    ax_plt2 = fig.add_subplot(gs2[1])
    ax_ilm1 = fig.add_subplot(gs2[2])
    ax_ilm2 = fig.add_subplot(gs2[3])
    ax_psf1 = fig.add_subplot(gs2[4])
    ax_psf2 = fig.add_subplot(gs2[5])

    c = int(z.mean()), int(y.mean())+s.pad, int(x.mean())+s.pad
    if s.image.shape[0] > 2*s.image.shape[1]//3:
        w = s.image.shape[2] - 2*s.pad
        h = 2*w//3
    else:
        h = s.image.shape[0] - 2*s.pad
        w = 3*h//2

    w,h = w//2, h//2
    xyslice = np.s_[slicez, c[1]-h:c[1]+h, c[2]-w:c[2]+w]
    yzslice = np.s_[c[0]-h:c[0]+h, c[1]-w:c[1]+w, slicex]

    #h = s.image.shape[2]/2 - s.image.shape[0]/2
    #slicer2 = np.s_[s.pad:-s.pad, s.pad:-s.pad, slicex]
    #slicer3 = np.s_[slicez, s.pad+h:-s.pad-h, s.pad:-s.pad]

    ax_plt1.imshow(1-s.obj.get_field()[xyslice], cmap=pl.cm.bone_r, vmin=0, vmax=1)
    ax_plt1.set_xticks([])
    ax_plt1.set_yticks([])
    ax_plt1.set_ylabel("Platonic", fontsize=22)
    ax_plt1.set_title("x-y", fontsize=24)
    ax_plt2.imshow(1-s._platonic_image()[yzslice], cmap=pl.cm.bone_r, vmin=0, vmax=1)
    ax_plt2.set_xticks([])
    ax_plt2.set_yticks([])
    ax_plt2.set_title("y-z", fontsize=24)

    ax_ilm1.imshow(s.ilm.get_field()[xyslice], cmap=pl.cm.bone_r)
    ax_ilm1.set_xticks([])
    ax_ilm1.set_yticks([])
    ax_ilm1.set_ylabel("ILM", fontsize=22)
    ax_ilm2.imshow(s.ilm.get_field()[yzslice], cmap=pl.cm.bone_r)
    ax_ilm2.set_xticks([])
    ax_ilm2.set_yticks([])

    t = s.ilm.get_field().copy()
    t *= 0
    t[c] = 1
    s.psf.set_tile(util.Tile(t.shape))
    psf = (s.psf.execute(t)+5e-5)**0.1

    ax_psf1.imshow(psf[xyslice], cmap=pl.cm.bone)
    ax_psf1.set_xticks([])
    ax_psf1.set_yticks([])
    ax_psf1.set_ylabel("PSF", fontsize=22)
    ax_psf2.imshow(psf[yzslice], cmap=pl.cm.bone)
    ax_psf2.set_xticks([])
    ax_psf2.set_yticks([])

    #=========================================================================
    #=========================================================================
    ax_zoom = fig.add_axes([0.48, 0.018, 0.45, 0.52])

    #s.model_to_true_image()
    im = s.image[slicer1]
    sh = np.array(im.shape)
    cx = x.mean()
    cy = y.mean()

    extent = [0,sh[0],0,sh[1]]
    ax_zoom.set_xticks([])
    ax_zoom.set_yticks([])
    ax_zoom.imshow(im, extent=extent, cmap=pl.cm.bone_r)
    ax_zoom.set_xlim(cx-12, cx+12)
    ax_zoom.set_ylim(cy-12, cy+12)
    ax_zoom.set_title("Sampled positions", fontsize=24)
    ax_zoom.hexbin(x,y, gridsize=32, mincnt=0, cmap=pl.cm.hot)

    zoom1 = zoomed_inset_axes(ax_zoom, 30, loc=3)
    zoom1.imshow(im, extent=extent, cmap=pl.cm.bone_r)
    zoom1.set_xlim(cx-1.0/6, cx+1.0/6)
    zoom1.set_ylim(cy-1.0/6, cy+1.0/6)
    zoom1.hexbin(x,y,gridsize=32, mincnt=5, cmap=pl.cm.hot)
    zoom1.set_xticks([])
    zoom1.set_yticks([])
    zoom1.hlines(cy-1.0/6 + 1.0/32, cx-1.0/6+5e-2, cx-1.0/6+5e-2+1e-1, lw=3)
    zoom1.text(cx-1.0/6 + 1.0/24, cy-1.0/6+5e-2, '0.1px')
    mark_inset(ax_zoom, zoom1, loc1=2, loc2=4, fc="none", ec="0.0")