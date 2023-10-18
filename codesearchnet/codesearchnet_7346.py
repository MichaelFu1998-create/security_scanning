def pty_fork(*args):
    """Runs a subprocess with a PTY attached via fork and exec.
    The output from the PTY is streamed through log_to_client.
    This should not be necessary for most subprocesses, we
    built this to handle Compose up which only streams pull
    progress if it is attached to a TTY."""

    updated_env = copy(os.environ)
    updated_env.update(get_docker_env())
    args += (updated_env,)
    executable = args[0]
    demote_fn = demote_to_user(get_config_value(constants.CONFIG_MAC_USERNAME_KEY))

    child_pid, pty_fd = pty.fork()
    if child_pid == 0:
        demote_fn()
        os.execle(_executable_path(executable), *args)
    else:
        child_process = psutil.Process(child_pid)
        terminal = os.fdopen(pty_fd, 'r', 0)
        with streaming_to_client():
            while child_process.status() == 'running':
                output = terminal.read(1)
                log_to_client(output)
        _, exit_code = os.waitpid(child_pid, 0)
        if exit_code != 0:
            raise subprocess.CalledProcessError(exit_code, ' '.join(args[:-1]))