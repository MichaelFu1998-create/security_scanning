def encapsulate_string(raw_string):
        """
        Encapsulate characters to make markdown look as expected.

        :param str raw_string: string to encapsulate
        :rtype: str
        :return: encapsulated input string
        """

        raw_string.replace('\\', '\\\\')
        enc_string = re.sub("([<>*_()\[\]#])", r"\\\1", raw_string)
        return enc_string