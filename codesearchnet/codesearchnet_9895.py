def parse_response(gdb_mi_text):
    """Parse gdb mi text and turn it into a dictionary.

    See https://sourceware.org/gdb/onlinedocs/gdb/GDB_002fMI-Stream-Records.html#GDB_002fMI-Stream-Records
    for details on types of gdb mi output.

    Args:
        gdb_mi_text (str): String output from gdb

    Returns:
        dict with the following keys:
        type (either 'notify', 'result', 'console', 'log', 'target', 'done'),
        message (str or None),
        payload (str, list, dict, or None)
    """
    stream = StringStream(gdb_mi_text, debug=_DEBUG)

    if _GDB_MI_NOTIFY_RE.match(gdb_mi_text):
        token, message, payload = _get_notify_msg_and_payload(gdb_mi_text, stream)
        return {
            "type": "notify",
            "message": message,
            "payload": payload,
            "token": token,
        }

    elif _GDB_MI_RESULT_RE.match(gdb_mi_text):
        token, message, payload = _get_result_msg_and_payload(gdb_mi_text, stream)
        return {
            "type": "result",
            "message": message,
            "payload": payload,
            "token": token,
        }

    elif _GDB_MI_CONSOLE_RE.match(gdb_mi_text):
        return {
            "type": "console",
            "message": None,
            "payload": _GDB_MI_CONSOLE_RE.match(gdb_mi_text).groups()[0],
        }

    elif _GDB_MI_LOG_RE.match(gdb_mi_text):
        return {
            "type": "log",
            "message": None,
            "payload": _GDB_MI_LOG_RE.match(gdb_mi_text).groups()[0],
        }

    elif _GDB_MI_TARGET_OUTPUT_RE.match(gdb_mi_text):
        return {
            "type": "target",
            "message": None,
            "payload": _GDB_MI_TARGET_OUTPUT_RE.match(gdb_mi_text).groups()[0],
        }

    elif response_is_finished(gdb_mi_text):
        return {"type": "done", "message": None, "payload": None}

    else:
        # This was not gdb mi output, so it must have just been printed by
        # the inferior program that's being debugged
        return {"type": "output", "message": None, "payload": gdb_mi_text}