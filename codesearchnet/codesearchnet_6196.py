def read_timeout_value_header(timeoutvalue):
    """Return -1 if infinite, else return numofsecs."""
    timeoutsecs = 0
    timeoutvaluelist = timeoutvalue.split(",")
    for timeoutspec in timeoutvaluelist:
        timeoutspec = timeoutspec.strip()
        if timeoutspec.lower() == "infinite":
            return -1
        else:
            listSR = reSecondsReader.findall(timeoutspec)
            for secs in listSR:
                timeoutsecs = int(secs)
                if timeoutsecs > MAX_FINITE_TIMEOUT_LIMIT:
                    return -1
                if timeoutsecs != 0:
                    return timeoutsecs
    return None