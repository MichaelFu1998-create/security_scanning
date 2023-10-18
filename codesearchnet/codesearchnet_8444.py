def err(txt):
    """Print, emphasized 'error', the given 'txt' message"""

    print("%s# %s%s%s" % (PR_ERR_CC, get_time_stamp(), txt, PR_NC))
    sys.stdout.flush()