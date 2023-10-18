def check_tracer_for_light_profile(func):
    """If none of the tracer's galaxies have a light profile, it image-plane image cannot be computed. This wrapper \
    makes this property return *None*.

    Parameters
    ----------
    func : (self) -> Object
        A property function that requires galaxies to have a mass profile.
    """

    @wraps(func)
    def wrapper(self):
        """

        Parameters
        ----------
        self

        Returns
        -------
            A value or coordinate in the same coordinate system as those passed in.
        """

        if self.has_light_profile is True:
            return func(self)
        else:
            return None

    return wrapper