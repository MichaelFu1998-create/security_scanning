def execute(cmd=None, shell=True, echo=True):
    """
    Execute the given 'cmd'

    @returns (rcode, stdout, stderr)
    """
    if echo:
        cij.emph("cij.util.execute: shell: %r, cmd: %r" % (shell, cmd))

    rcode = 1
    stdout, stderr = ("", "")

    if cmd:
        if shell:
            cmd = " ".join(cmd)

        proc = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=shell, close_fds=True)
        stdout, stderr = proc.communicate()
        rcode = proc.returncode

    if rcode and echo:
        cij.warn("cij.util.execute: stdout: %s" % stdout)
        cij.err("cij.util.execute: stderr: %s" % stderr)
        cij.err("cij.util.execute: rcode: %s" % rcode)

    return rcode, stdout, stderr