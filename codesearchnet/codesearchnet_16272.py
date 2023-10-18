def run_commands(commands, settings):
    """
    Runs the commands supplied as an argument
    It will exit the program if the commands return a
    non-zero code

    Args:
        the commands to run
        The settings dictionary
    """
    sprint = settings["sprint"]
    quiet = settings["quiet"]
    error = settings["error"]
    enhanced_errors = True
    the_shell = None
    if settings["no_enhanced_errors"]:
        enhanced_errors = False
    if "shell" in settings:
        the_shell = settings["shell"]
    windows_p = sys.platform == "win32"

    STDOUT = None
    STDERR = None
    if quiet:
        STDOUT = PIPE
        STDERR = PIPE

    commands = commands.rstrip()
    sprint("About to run commands '{}'".format(commands), level="verbose")
    if not quiet:
        sprint(commands)

    if the_shell:
        tmp = shlex.split(the_shell)
        the_shell = tmp[0]
        tmp = tmp[1:]
        if enhanced_errors and not windows_p:
            tmp.append("-e")
        tmp.append(commands)
        commands = tmp
    else:
        if enhanced_errors and not windows_p:
            commands = ["-e", commands]

    p = Popen(commands, shell=True, stdout=STDOUT, stderr=STDERR,
              executable=the_shell)
    out, err = p.communicate()
    if p.returncode:
        if quiet:
            error(err.decode(locale.getpreferredencoding()))
        error("Command failed to run")
        sys.exit(1)