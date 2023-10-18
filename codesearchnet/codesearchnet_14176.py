def ensure_pycairo_context(self, ctx):
        """
        If ctx is a cairocffi Context convert it to a PyCairo Context
        otherwise return the original context

        :param ctx:
        :return:
        """
        if self.cairocffi and isinstance(ctx, self.cairocffi.Context):
            from shoebot.util.cairocffi.cairocffi_to_pycairo import _UNSAFE_cairocffi_context_to_pycairo
            return _UNSAFE_cairocffi_context_to_pycairo(ctx)
        else:
            return ctx