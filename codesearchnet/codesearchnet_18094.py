def scramble_positions(p, delete_frac=0.1):
    """randomly deletes particles and adds 1-px noise for a realistic
    initial featuring guess"""
    probs = [1-delete_frac, delete_frac]
    m = np.random.choice([True, False], p.shape[0], p=probs)
    jumble = np.random.randn(m.sum(), 3)
    return p[m] + jumble