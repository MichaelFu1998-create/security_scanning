def parse_epsv_response(s):
        """
        Parsing `EPSV` (`message (|||port|)`) response.

        :param s: response line
        :type s: :py:class:`str`

        :return: (ip, port)
        :rtype: (:py:class:`None`, :py:class:`int`)
        """
        matches = tuple(re.finditer(r"\((.)\1\1\d+\1\)", s))
        s = matches[-1].group()
        port = int(s[4:-2])
        return None, port