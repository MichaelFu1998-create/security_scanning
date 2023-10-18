def touch(self, name, args=None):
        """Apply touch actions on devices. Such as, tap/doubleTap/press/pinch/rotate/drag.
            See more on https://github.com/alibaba/macaca/issues/366.

        Support:
            Android iOS

        Args:
            name(str): Name of the action
            args(dict): Arguments of the action

        Returns:
            WebDriver Object.

        Raises:
            WebDriverException.
        """
        if isinstance(name, list) and not isinstance(name, str):
            for obj in name:
                obj['element'] = self.element_id
            actions = name
        elif isinstance(name, str):
            if not args:
                args = {}
            args['type'] = name
            args['element'] = self.element_id
            actions = [args]
        else:
            raise TypeError('Invalid parameters.')
        self._driver._execute(Command.PERFORM_ACTIONS, {
            'actions': actions
        })