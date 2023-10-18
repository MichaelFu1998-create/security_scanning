def correspond(text):
    """Communicate with the child process without closing stdin."""
    if text:
        subproc.stdin.write(text)
    subproc.stdin.flush()
    return get_lines()