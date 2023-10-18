def parse_list_line_windows(self, b):
        """
        Parsing Microsoft Windows `dir` output

        :param b: response line
        :type b: :py:class:`bytes` or :py:class:`str`

        :return: (path, info)
        :rtype: (:py:class:`pathlib.PurePosixPath`, :py:class:`dict`)
        """
        line = b.decode(encoding=self.encoding).rstrip("\r\n")
        date_time_end = line.index("M")
        date_time_str = line[:date_time_end + 1].strip().split(" ")
        date_time_str = " ".join([x for x in date_time_str if len(x) > 0])
        line = line[date_time_end + 1:].lstrip()
        with setlocale("C"):
            strptime = datetime.datetime.strptime
            date_time = strptime(date_time_str, "%m/%d/%Y %I:%M %p")
        info = {}
        info["modify"] = self.format_date_time(date_time)
        next_space = line.index(" ")
        if line.startswith("<DIR>"):
            info["type"] = "dir"
        else:
            info["type"] = "file"
            info["size"] = line[:next_space].replace(",", "")
            if not info["size"].isdigit():
                raise ValueError
        # This here could cause a problem if a filename started with
        # whitespace, but if we were to try to detect such a condition
        # we would have to make strong assumptions about the input format
        filename = line[next_space:].lstrip()
        if filename == "." or filename == "..":
            raise ValueError
        return pathlib.PurePosixPath(filename), info