def _filter_binding(self, binding):
        """
        Filter binding from ISBN record. In MARC XML / OAI, the binding
        information is stored in same subrecord as ISBN.

        Example:
            ``<subfield code="a">80-251-0225-4 (brož.) :</subfield>`` ->
            ``brož.``.
        """
        binding = binding.strip().split(" ", 1)[-1]  # isolate bind. from ISBN
        binding = remove_hairs_fn(binding)  # remove special chars from binding

        return binding.split(":")[-1].strip()