def write(self, data):
        """Just quote out stuff before sending it out"""
        args = parse_qs(self.handler.environ.get("QUERY_STRING"))
        if "i" in args:
            i = args["i"]
        else:
            i = "0"
        # TODO: don't we need to quote this data in here ?
        super(JSONPolling, self).write("io.j[%s]('%s');" % (i, data))