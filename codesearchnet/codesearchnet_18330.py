def path_required(func):
    """Decorate methods when repository path is required."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.path is None:
            warnings.warn('Must load (Repository.load_repository) or initialize (Repository.create_repository) the repository first !')
            return
        return func(self, *args, **kwargs)
    return wrapper