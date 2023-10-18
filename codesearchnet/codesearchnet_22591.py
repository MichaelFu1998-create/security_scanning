def guid(*args):
    """
    Generates a universally unique ID.
    Any arguments only create more randomness.
    """
    t = float(time.time() * 1000)
    r = float(random.random()*10000000000000)

    a = random.random() * 10000000000000
    data = str(t) + ' ' + str(r) + ' ' + str(a) + ' ' + str(args)
    data = hashlib.md5(data.encode()).hexdigest()[:10]

    return data