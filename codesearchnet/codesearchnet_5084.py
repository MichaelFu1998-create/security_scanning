def _CCompiler_spawn_silent(cmd, dry_run=None):
    """Spawn a process, and eat the stdio."""
    proc = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate()
    if proc.returncode:
        raise DistutilsExecError(err)