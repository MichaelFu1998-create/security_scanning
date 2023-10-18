def yield_tag(self, target=None, label=None):
        """
        Returns a new Tag containing the bumped target and/or the bumped label
        """
        if target is None and label is None:
            raise ValueError('`target` and/or `label` must be specified')
        if label is None:
            return self._yield_from_target(target)
        if target is None:
            return self._yield_from_label(label)
        return self._yield_from_target_and_label(target, label)