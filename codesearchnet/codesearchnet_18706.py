def run_shell_command(commands, **kwargs):
    """Run a shell command."""
    p = subprocess.Popen(commands,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         **kwargs)
    output, error = p.communicate()
    return p.returncode, output, error