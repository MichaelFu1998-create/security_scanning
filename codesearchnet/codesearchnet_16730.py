def _get_dynamic_base(self, bases_):
        """Create or get the base space from a list of spaces

        if a direct base space in `bases` is dynamic, replace it with
        its base.
        """
        bases = tuple(
            base.bases[0] if base.is_dynamic() else base for base in bases_
        )

        if len(bases) == 1:
            return bases[0]

        elif len(bases) > 1:
            return self.model.get_dynamic_base(bases)

        else:
            RuntimeError("must not happen")