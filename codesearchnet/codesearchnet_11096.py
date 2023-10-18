def get_runnable_effects(self) -> List[Effect]:
        """
        Returns all runnable effects in the project.

        :return: List of all runnable effects
        """
        return [effect for name, effect in self._effects.items() if effect.runnable]