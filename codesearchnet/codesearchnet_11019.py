def resolve_loader(self, meta: SceneDescription):
        """
        Resolve scene loader based on file extension
        """
        for loader_cls in self._loaders:
            if loader_cls.supports_file(meta):
                meta.loader_cls = loader_cls
                break
        else:
            raise ImproperlyConfigured(
                "Scene {} has no loader class registered. Check settings.SCENE_LOADERS".format(meta.path))