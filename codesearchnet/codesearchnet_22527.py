def split_path(path):
        """
        Helper method for absolute and relative paths resolution
        Split passed path and return each directory parts

        example: "/usr/share/dir"
        return: ["usr", "share", "dir"]

        @type path: one of (unicode, str)
        @rtype: list
        """
        result_parts = []
        #todo: check loops
        while path != "/":
            parts = os.path.split(path)
            if parts[1] == path:
                result_parts.insert(0, parts[1])
                break
            elif parts[0] == path:
                result_parts.insert(0, parts[0])
                break
            else:
                path = parts[0]
                result_parts.insert(0, parts[1])
        return result_parts