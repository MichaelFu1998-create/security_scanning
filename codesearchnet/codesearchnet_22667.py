def arkt_to_unixt(ark_timestamp):
    """ convert ark timestamp to unix timestamp"""
    res = datetime.datetime(2017, 3, 21, 15, 55, 44) + datetime.timedelta(seconds=ark_timestamp)
    return res.timestamp()