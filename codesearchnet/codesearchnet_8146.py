def clone(self):
        """
        Return an independent copy of this layout with a completely separate
        color_list and no drivers.
        """
        args = {k: getattr(self, k) for k in self.CLONE_ATTRS}
        args['color_list'] = copy.copy(self.color_list)
        return self.__class__([], **args)