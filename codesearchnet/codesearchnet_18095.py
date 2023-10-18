def create_img():
    """Creates an image, as a `peri.util.Image`, which is similar
    to the image in the tutorial"""
    # 1. particles + coverslip
    rad = 0.5 * np.random.randn(POS.shape[0]) + 4.5  # 4.5 +- 0.5 px particles
    part = objs.PlatonicSpheresCollection(POS, rad, zscale=0.89)
    slab = objs.Slab(zpos=4.92, angles=(-4.7e-3, -7.3e-4))
    objects = comp.ComponentCollection([part, slab], category='obj')

    # 2. psf, ilm
    p = exactpsf.FixedSSChebLinePSF(kfki=1.07, zslab=-29.3, alpha=1.17,
            n2n1=0.98, sigkf=-0.33, zscale=0.89, laser_wavelength=0.45)
    i = ilms.BarnesStreakLegPoly2P1D(npts=(16,10,8,4), zorder=8)
    b = ilms.LegendrePoly2P1D(order=(7,2,2), category='bkg')
    off = comp.GlobalScalar(name='offset', value=-2.11)
    mdl = models.ConfocalImageModel()
    st = states.ImageState(util.NullImage(shape=[48,64,64]),
            [objects, p, i, b, off], mdl=mdl, model_as_data=True)
    b.update(b.params, BKGVALS)
    i.update(i.params, ILMVALS)
    im = st.model + np.random.randn(*st.model.shape) * 0.03
    return util.Image(im)