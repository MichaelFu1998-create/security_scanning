def cmd_kill(opts):
    """Kill some or all containers
    """
    kill_signal = opts.signal if hasattr(opts, 'signal') else "SIGKILL"
    __with_containers(opts, Blockade.kill, signal=kill_signal)