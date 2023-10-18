def norm(field, vmin=0, vmax=255):
    """Truncates field to 0,1; then normalizes to a uin8 on [0,255]"""
    field = 255*np.clip(field, 0, 1)
    field = field.astype('uint8')
    return field