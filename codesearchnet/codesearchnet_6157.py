def lock_string(lock_dict):
    """Return readable rep."""
    if not lock_dict:
        return "Lock: None"

    if lock_dict["expire"] < 0:
        expire = "Infinite ({})".format(lock_dict["expire"])
    else:
        expire = "{} (in {} seconds)".format(
            util.get_log_time(lock_dict["expire"]), lock_dict["expire"] - time.time()
        )

    return "Lock(<{}..>, '{}', {}, {}, depth-{}, until {}".format(
        # first 4 significant token characters
        lock_dict.get("token", "?" * 30)[18:22],
        lock_dict.get("root"),
        lock_dict.get("principal"),
        lock_dict.get("scope"),
        lock_dict.get("depth"),
        expire,
    )