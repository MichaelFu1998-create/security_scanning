def brightness(level=100, group=0):
    """ Assumes level is out of 100 """
    if level not in range(0,101):
        raise Exception("Brightness must be value between 0 and 100")
    b = int(floor(level / 4.0) + 2) #lights want values 2-27
    return (COMMANDS['ON'][group], Command(0x4E, b))