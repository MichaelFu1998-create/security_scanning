def warmness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Warmness must be value between 0 and 100")
    b = int(floor(level / 10.0)) #lights have 10 levels of warmness
    commands = list(coolest(group))
    for i in range(0, b):
        commands.append(COMMANDS['WARMER'])
    return tuple(commands)