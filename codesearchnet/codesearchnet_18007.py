def crb_compare(state0, samples0, state1, samples1, crb0=None, crb1=None,
        zlayer=None, xlayer=None):
    """
    To run, do:

    s,h = pickle...
    s1,h1 = pickle...
        i.e. /media/scratch/bamf/vacancy/vacancy_zoom-1.tif_t002.tif-featured-v2.pkl
        i.e. /media/scratch/bamf/frozen-particles/0.tif-featured-full.pkl
    crb0 = diag_crb_particles(s); crb1 = diag_crb_particles(s1)
    crb_compare(s,h[-25:],s1,h1[-25:], crb0, crb1)
    """
    s0 = state0
    s1 = state1
    h0 = np.array(samples0)
    h1 = np.array(samples1)

    slicez = zlayer or s0.image.shape[0]//2
    slicex = xlayer or s0.image.shape[2]//2
    slicer1 = np.s_[slicez,s0.pad:-s0.pad,s0.pad:-s0.pad]
    slicer2 = np.s_[s0.pad:-s0.pad,s0.pad:-s0.pad,slicex]
    center = (slicez, s0.image.shape[1]//2, slicex)

    mu0 = h0.mean(axis=0)
    mu1 = h1.mean(axis=0)

    std0 = h0.std(axis=0)
    std1 = h1.std(axis=0)

    mask0 = (s0.state[s0.b_typ]==1.) & (
        analyze.trim_box(s0, mu0[s0.b_pos].reshape(-1,3)))
    mask1 = (s1.state[s1.b_typ]==1.) & (
        analyze.trim_box(s1, mu1[s1.b_pos].reshape(-1,3)))
    active0 = np.arange(s0.N)[mask0]#s0.state[s0.b_typ]==1.]
    active1 = np.arange(s1.N)[mask1]#s1.state[s1.b_typ]==1.]

    pos0 = mu0[s0.b_pos].reshape(-1,3)[active0]
    pos1 = mu1[s1.b_pos].reshape(-1,3)[active1]
    rad0 = mu0[s0.b_rad][active0]
    rad1 = mu1[s1.b_rad][active1]

    link = analyze.nearest(pos0, pos1)
    dpos = pos0 - pos1[link]
    drad = rad0 - rad1[link]

    drift = dpos.mean(axis=0)
    log.info('drift {}'.format(drift))

    dpos -= drift

    fig = pl.figure(figsize=(24,10))

    #=========================================================================
    #=========================================================================
    gs0 = ImageGrid(fig, rect=[0.02, 0.4, 0.4, 0.60], nrows_ncols=(2,3), axes_pad=0.1)

    lbl(gs0[0], 'A')
    for i,slicer in enumerate([slicer1, slicer2]):
        ax_real = gs0[3*i+0]
        ax_fake = gs0[3*i+1]
        ax_diff = gs0[3*i+2]

        diff0 = s0.get_model_image() - s0.image
        diff1 = s1.get_model_image() - s1.image
        a = (s0.image - s1.image)
        b = (s0.get_model_image() - s1.get_model_image())
        c = (diff0 - diff1)

        ptp = 0.7*max([np.abs(a).max(), np.abs(b).max(), np.abs(c).max()])
        cmap = pl.cm.RdBu_r
        ax_real.imshow(a[slicer], cmap=cmap, vmin=-ptp, vmax=ptp)
        ax_real.set_xticks([])
        ax_real.set_yticks([])
        ax_fake.imshow(b[slicer], cmap=cmap, vmin=-ptp, vmax=ptp)
        ax_fake.set_xticks([])
        ax_fake.set_yticks([])
        ax_diff.imshow(c[slicer], cmap=cmap, vmin=-ptp, vmax=ptp)#cmap=pl.cm.RdBu, vmin=-1.0, vmax=1.0)
        ax_diff.set_xticks([])
        ax_diff.set_yticks([])

        if i == 0:
            ax_real.set_title(r"$\Delta$ Confocal image", fontsize=24)
            ax_fake.set_title(r"$\Delta$ Model image", fontsize=24)
            ax_diff.set_title(r"$\Delta$ Difference", fontsize=24)
            ax_real.set_ylabel('x-y')
        else:
            ax_real.set_ylabel('x-z')

    #=========================================================================
    #=========================================================================
    gs1 = GridSpec(1,3, left=0.05, bottom=0.125, right=0.42, top=0.37,
                wspace=0.15, hspace=0.05)

    spos0 = std0[s0.b_pos].reshape(-1,3)[active0]
    spos1 = std1[s1.b_pos].reshape(-1,3)[active1]
    srad0 = std0[s0.b_rad][active0]
    srad1 = std1[s1.b_rad][active1]

    def hist(ax, vals, bins, *args, **kwargs):
        y,x = np.histogram(vals, bins=bins)
        x = (x[1:] + x[:-1])/2
        y /= len(vals)
        ax.plot(x,y, *args, **kwargs)

    def pp(ind, tarr, tsim, tcrb, var='x'):
        bins = 10**np.linspace(-3, 0.0, 30)
        bin2 = 10**np.linspace(-3, 0.0, 100)
        bins = np.linspace(0.0, 0.2, 30)
        bin2 = np.linspace(0.0, 0.2, 100)
        xlim = (0.0, 0.12)
        #xlim = (1e-3, 1e0)
        ylim = (1e-2, 30)

        ticks = ticker.FuncFormatter(lambda x, pos: '{:0.0f}'.format(np.log10(x)))
        scaler = lambda x: x #np.log10(x)

        ax_crb = pl.subplot(gs1[0,ind])
        ax_crb.hist(scaler(np.abs(tarr)), bins=bins,
                normed=True, alpha=0.7, histtype='stepfilled', lw=1)
        ax_crb.hist(scaler(np.abs(tcrb)).ravel(), bins=bin2,
                normed=True, alpha=1.0, histtype='step', ls='solid', lw=1.5, color='k')
        ax_crb.hist(scaler(np.abs(tsim).ravel()), bins=bin2,
                normed=True, alpha=1.0, histtype='step', lw=3)
        ax_crb.set_xlabel(r"$\Delta = |%s(t_1) - %s(t_0)|$" % (var,var), fontsize=24)
        #ax_crb.semilogx()
        ax_crb.set_xlim(xlim)
        #ax_crb.semilogy()
        #ax_crb.set_ylim(ylim)
        #ax_crb.xaxis.set_major_formatter(ticks)
        ax_crb.grid(b=False, which='both', axis='both')

        if ind == 0:
            lbl(ax_crb, 'B')
            ax_crb.set_ylabel(r"$P(\Delta)$")
        else:
            ax_crb.set_yticks([])

        ax_crb.locator_params(axis='x', nbins=3)

    f,g = 1.5, 1.95
    sim = f*sim_crb_diff(spos0[:,1], spos1[:,1][link])
    crb = g*sim_crb_diff(crb0[0][:,1][active0], crb1[0][:,1][active1][link])
    pp(0, dpos[:,1], sim, crb, 'x')

    sim = f*sim_crb_diff(spos0[:,0], spos1[:,0][link])
    crb = g*sim_crb_diff(crb0[0][:,0][active0], crb1[0][:,0][active1][link])
    pp(1, dpos[:,0], sim, crb, 'z')

    sim = f*sim_crb_diff(srad0, srad1[link])
    crb = g*sim_crb_diff(crb0[1][active0], crb1[1][active1][link])
    pp(2, drad, sim, crb, 'a')

    #ax_crb_r.locator_params(axis='both', nbins=3)
    #gs1.tight_layout(fig)

    #=========================================================================
    #=========================================================================
    gs2 = GridSpec(2,2, left=0.48, bottom=0.12, right=0.99, top=0.95,
                wspace=0.35, hspace=0.35)

    ax_hist = pl.subplot(gs2[0,0])
    ax_hist.hist(std0[s0.b_pos], bins=np.logspace(-3.0, 0, 50), alpha=0.7, label='POS', histtype='stepfilled')
    ax_hist.hist(std0[s0.b_rad], bins=np.logspace(-3.0, 0, 50), alpha=0.7, label='RAD', histtype='stepfilled')
    ax_hist.set_xlim((10**-3.0, 1))
    ax_hist.semilogx()
    ax_hist.set_xlabel(r"$\bar{\sigma}$")
    ax_hist.set_ylabel(r"$P(\bar{\sigma})$")
    ax_hist.legend(loc='upper right')
    lbl(ax_hist, 'C')

    imdiff = ((s0.get_model_image() - s0.image)/s0._sigma_field)[s0.image_mask==1.].ravel()
    mu = imdiff.mean()
    #sig = imdiff.std()
    #print mu, sig
    x = np.linspace(-5,5,10000)

    ax_diff = pl.subplot(gs2[0,1])
    ax_diff.plot(x, 1.0/np.sqrt(2*np.pi) * np.exp(-(x-mu)**2 / 2), '-', alpha=0.7, color='k', lw=2)
    ax_diff.hist(imdiff, bins=1000, histtype='step', alpha=0.7, normed=True)
    ax_diff.semilogy()
    ax_diff.set_ylabel(r"$P(\delta)$")
    ax_diff.set_xlabel(r"$\delta = (M_i - d_i)/\sigma_i$")
    ax_diff.locator_params(axis='x', nbins=5)
    ax_diff.grid(b=False, which='minor', axis='y')
    ax_diff.set_xlim(-5, 5)
    ax_diff.set_ylim(1e-4, 1e0)
    lbl(ax_diff, 'D')

    pos = mu0[s0.b_pos].reshape(-1,3)
    rad = mu0[s0.b_rad]
    mask = analyze.trim_box(s0, pos)
    pos = pos[mask]
    rad = rad[mask]

    gx, gy = analyze.gofr(pos, rad, mu0[s0.b_zscale][0], resolution=5e-2,mask_start=0.5)
    mask = gx < 5
    gx = gx[mask]
    gy = gy[mask]
    ax_gofr = pl.subplot(gs2[1,0])
    ax_gofr.plot(gx, gy, '-', lw=1)
    ax_gofr.set_xlabel(r"$r/a$")
    ax_gofr.set_ylabel(r"$g(r/a)$")
    ax_gofr.locator_params(axis='both', nbins=5)
    #ax_gofr.semilogy()
    lbl(ax_gofr, 'E')

    gx, gy = analyze.gofr(pos, rad, mu0[s0.b_zscale][0], method='surface')
    mask = gx < 5
    gx = gx[mask]
    gy = gy[mask]
    gy[gy <= 0.] = gy[gy>0].min()
    ax_gofrs = pl.subplot(gs2[1,1])
    ax_gofrs.plot(gx, gy, '-', lw=1)
    ax_gofrs.set_xlabel(r"$r/a$")
    ax_gofrs.set_ylabel(r"$g_{\rm{surface}}(r/a)$")
    ax_gofrs.locator_params(axis='both', nbins=5)
    ax_gofrs.grid(b=False, which='minor', axis='y')
    #ax_gofrs.semilogy()
    lbl(ax_gofrs, 'F')

    ylim = ax_gofrs.get_ylim()
    ax_gofrs.set_ylim(gy.min(), ylim[1])