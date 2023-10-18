def get_hash(x):
    """Return hash of x."""
    if isinstance(x, str):
        return hash(x)
    elif isinstance(x, dict):
        return hash(yaml.dump(x))