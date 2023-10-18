def _sample_chain(args):
    """Sample a single chain for OptGPSampler.

    center and n_samples are updated locally and forgotten afterwards.

    """

    n, idx = args       # has to be this way to work in Python 2.7
    center = sampler.center
    np.random.seed((sampler._seed + idx) % np.iinfo(np.int32).max)
    pi = np.random.randint(sampler.n_warmup)

    prev = sampler.warmup[pi, ]
    prev = step(sampler, center, prev - center, 0.95)

    n_samples = max(sampler.n_samples, 1)
    samples = np.zeros((n, center.shape[0]))

    for i in range(1, sampler.thinning * n + 1):
        pi = np.random.randint(sampler.n_warmup)
        delta = sampler.warmup[pi, ] - center

        prev = step(sampler, prev, delta)

        if sampler.problem.homogeneous and (
                n_samples * sampler.thinning % sampler.nproj == 0):
            prev = sampler._reproject(prev)
            center = sampler._reproject(center)

        if i % sampler.thinning == 0:
            samples[i//sampler.thinning - 1, ] = prev

        center = ((n_samples * center) / (n_samples + 1) +
                  prev / (n_samples + 1))
        n_samples += 1

    return (sampler.retries, samples)