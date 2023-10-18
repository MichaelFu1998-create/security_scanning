def env():
    """Verify SSH variables and construct exported variables"""

    ssh = cij.env_to_dict(PREFIX, REQUIRED)
    if "KEY" in ssh:
        ssh["KEY"] = cij.util.expand_path(ssh["KEY"])

    if cij.ENV.get("SSH_PORT") is None:
        cij.ENV["SSH_PORT"] = "22"
        cij.warn("cij.ssh.env: SSH_PORT was not set, assigned: %r" % (
            cij.ENV.get("SSH_PORT")
        ))

    if cij.ENV.get("SSH_CMD_TIME") is None:
        cij.ENV["SSH_CMD_TIME"] = "1"
        cij.warn("cij.ssh.env: SSH_CMD_TIME was not set, assigned: %r" % (
            cij.ENV.get("SSH_CMD_TIME")
        ))

    return 0