def create_comparison_state(image, position, radius=5.0, snr=20,
        method='constrained-cubic', extrapad=2, zscale=1.0):
    """
    Take a platonic image and position and create a state which we can
    use to sample the error for peri. Also return the blurred platonic
    image so we can vary the noise on it later
    """
    # first pad the image slightly since they are pretty small
    image = common.pad(image, extrapad, 0)

    # place that into a new image at the expected parameters
    s = init.create_single_particle_state(imsize=np.array(image.shape), sigma=1.0/snr,
            radius=radius, psfargs={'params': np.array([2.0, 1.0, 3.0]), 'error': 1e-6, 'threads': 2},
            objargs={'method': method}, stateargs={'sigmapad': False, 'pad': 4, 'zscale': zscale})
    s.obj.pos[0] = position + s.pad + extrapad
    s.reset()
    s.model_to_true_image()

    timage = 1-np.pad(image, s.pad, mode='constant', constant_values=0)
    timage = s.psf.execute(timage)
    return s, timage[s.inner]