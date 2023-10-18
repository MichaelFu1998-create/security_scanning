def find_gromacs_command(commands):
    """Return *driver* and *name* of the first command that can be found on :envvar:`PATH`"""

    # We could try executing 'name' or 'driver name' but to keep things lean we
    # just check if the executables can be found and then hope for the best.

    commands = utilities.asiterable(commands)
    for command in commands:
        try:
            driver, name = command.split()
        except ValueError:
            driver, name = None, command

        executable = driver if driver else name
        if utilities.which(executable):
            break
    else:
        raise OSError(errno.ENOENT, "No Gromacs executable found in", ", ".join(commands))

    return driver, name