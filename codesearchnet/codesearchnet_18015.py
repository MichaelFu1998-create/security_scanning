def low_mem_sq(m, step=100000):
    """np.dot(m, m.T) with low mem usage, by doing it in small steps"""
    if not m.flags.c_contiguous:
        raise ValueError('m must be C ordered for this to work with less mem.')
    # -- can make this even faster with pre-allocating arrays, but not worth it
    # right now
    # mmt = np.zeros([m.shape[0], m.shape[0]])  #6us
    # mt_tmp = np.zeros([step, m.shape[0]])
    # for a in range(0, m.shape[1], step):
        # mx = min(a+step, m.shape[1])
        # mt_tmp[:mx-a,:] = m.T[a:mx]
        # # np.dot(m_tmp, m.T, out=mmt[a:mx])
        # # np.dot(m, m[a:mx].T, out=mmt[:, a:mx])
        # np.dot(m[:,a:mx], mt_tmp[:mx], out=mmt)
    # return mmt
    mmt = np.zeros([m.shape[0], m.shape[0]])  #6us
    # m_tmp = np.zeros([step, m.shape[1]])
    for a in range(0, m.shape[0], step):
        mx = min(a+step, m.shape[1])
        # m_tmp[:] = m[a:mx]
        # np.dot(m_tmp, m.T, out=mmt[a:mx])
        mmt[:, a:mx] = np.dot(m, m[a:mx].T)
    return mmt