def summary(self):
        """
        A succinct summary of the argument specifier. Unlike the repr,
        a summary does not have to be complete but must supply the
        most relevant information about the object to the user.
        """
        print("Items: %s" % len(self))
        varying_keys = ', '.join('%r' % k for k in self.varying_keys)
        print("Varying Keys: %s" % varying_keys)
        items = ', '.join(['%s=%r' % (k,v)
                           for (k,v) in self.constant_items])
        if self.constant_items:
            print("Constant Items: %s" % items)