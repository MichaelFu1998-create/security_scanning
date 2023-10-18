def parse_pasv_response(s):
        """
        Parsing `PASV` server response.

        :param s: response line
        :type s: :py:class:`str`

        :return: (ip, port)
        :rtype: (:py:class:`str`, :py:class:`int`)
        """
        sub, *_ = re.findall(r"[^(]*\(([^)]*)", s)
        nums = tuple(map(int, sub.split(",")))
        ip = ".".join(map(str, nums[:4]))
        port = (nums[4] << 8) | nums[5]
        return ip, port