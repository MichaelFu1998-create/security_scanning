def find_commands(command_dir: str) -> List[str]:
    """
    Get all command names in the a folder

    :return: List of commands names
    """
    if not command_dir:
        return []

    return [name for _, name, is_pkg in pkgutil.iter_modules([command_dir])
            if not is_pkg and not name.startswith('_')]