def rand_blend_mask(shape, rand=rand.uniform(-10, 10), **kwargs):
    """ random blending masks """
    # batch, channel = shape[0], shape[3]
    z = rand(shape[0])  # seed
    noise = snoise2dz((shape[1], shape[2]), z, **kwargs)

    return noise