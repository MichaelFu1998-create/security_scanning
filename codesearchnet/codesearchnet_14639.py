def get_passphrase(passphrase=None):
    """Return a passphrase as found in a passphrase.ghost file

    Lookup is done in three locations on non-Windows systems and two on Windows
    All:
        `cwd/passphrase.ghost`
        `~/.ghost/passphrase.ghost`
    Only non-Windows:
        `/etc/ghost/passphrase.ghost`
    """
    for passphrase_file_path in POTENTIAL_PASSPHRASE_LOCATIONS:
        if os.path.isfile(passphrase_file_path):
            with open(passphrase_file_path) as passphrase_file:
                return passphrase_file.read()
    return passphrase