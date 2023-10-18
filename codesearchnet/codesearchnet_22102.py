def yn_prompt(msg, default=True):
    """
    Prompts the user for yes or no.
    """
    ret = custom_prompt(msg, ["y", "n"], "y" if default else "n")
    if ret == "y":
        return True
    return False