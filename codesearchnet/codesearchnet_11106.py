def resolve_loader(self, meta: ProgramDescription):
        """
        Resolve program loader
        """
        if not meta.loader:
            meta.loader = 'single' if meta.path else 'separate'

        for loader_cls in self._loaders:
            if loader_cls.name == meta.loader:
                meta.loader_cls = loader_cls
                break
        else:
            raise ImproperlyConfigured(
                (
                    "Program {} has no loader class registered."
                    "Check PROGRAM_LOADERS or PROGRAM_DIRS"
                ).format(meta.path)
            )