def provider(workdir, commit=True, **kwargs):
    """Factory for the correct SCM provider in `workdir`."""
    return SCM_PROVIDER[auto_detect(workdir)](workdir, commit=commit, **kwargs)