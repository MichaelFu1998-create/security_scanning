def warn(txt):
    """Print, emphasized 'warning', the given 'txt' message"""

    print("%s# %s%s%s" % (PR_WARN_CC, get_time_stamp(), txt, PR_NC))
    sys.stdout.flush()