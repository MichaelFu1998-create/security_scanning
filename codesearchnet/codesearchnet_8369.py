def get_shared_secret(priv, pub):
    """ Derive the share secret between ``priv`` and ``pub``

        :param `Base58` priv: Private Key
        :param `Base58` pub: Public Key
        :return: Shared secret
        :rtype: hex

        The shared secret is generated such that::

            Pub(Alice) * Priv(Bob) = Pub(Bob) * Priv(Alice)

    """
    pub_point = pub.point()
    priv_point = int(repr(priv), 16)
    res = pub_point * priv_point
    res_hex = "%032x" % res.x()
    # Zero padding
    res_hex = "0" * (64 - len(res_hex)) + res_hex
    return res_hex