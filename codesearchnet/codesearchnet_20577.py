def nifti_out(f):
    """ Picks a function whose first argument is an `img`, processes its
    data and returns a numpy array. This decorator wraps this numpy array
    into a nibabel.Nifti1Image."""
    @wraps(f)
    def wrapped(*args, **kwargs):
        r = f(*args, **kwargs)

        img = read_img(args[0])
        return nib.Nifti1Image(r, affine=img.get_affine(), header=img.header)

    return wrapped