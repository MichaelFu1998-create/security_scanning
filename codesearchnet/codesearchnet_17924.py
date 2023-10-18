def generate_sphere(radius):
    """Generates a centered boolean mask of a 3D sphere"""
    rint = np.ceil(radius).astype('int')
    t = np.arange(-rint, rint+1, 1)
    x,y,z = np.meshgrid(t, t, t, indexing='ij')
    r = np.sqrt(x*x + y*y + z*z)
    sphere = r < radius
    return sphere