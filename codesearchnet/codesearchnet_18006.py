def sim_crb_diff(std0, std1, N=10000):
    """ each element of std0 should correspond with the element of std1 """
    a = std0*np.random.randn(N, len(std0))
    b = std1*np.random.randn(N, len(std1))
    return a - b