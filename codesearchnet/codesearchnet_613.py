def prepro(I):
    """Prepro 210x160x3 uint8 frame into 6400 (80x80) 1D float vector."""
    I = I[35:195]
    I = I[::2, ::2, 0]
    I[I == 144] = 0
    I[I == 109] = 0
    I[I != 0] = 1
    return I.astype(np.float).ravel()