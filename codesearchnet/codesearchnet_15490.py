def add_mixin(self, mixin):
        """Add mixin to scope
        Args:
            mixin (Mixin): Mixin object
        """
        raw = mixin.tokens[0][0].raw()
        if raw in self._mixins:
            self._mixins[raw].append(mixin)
        else:
            self._mixins[raw] = [mixin]