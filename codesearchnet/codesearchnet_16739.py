def evalrepr(self):
        """Evaluable repr"""
        args = [repr(arg) for arg in get_interfaces(self.argvalues)]
        param = ", ".join(args)
        return "%s(%s)" % (self.parent.evalrepr, param)