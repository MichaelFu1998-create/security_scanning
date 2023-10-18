def check_tracer_for_mass_profile(func):
    """If none of the tracer's galaxies have a mass profile, it surface density, potential and deflections cannot \
    be computed. This wrapper makes these properties return *None*.

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

        if self.has_mass_profile is True:
            return func(self)
        else:
            return None

    return wrapper