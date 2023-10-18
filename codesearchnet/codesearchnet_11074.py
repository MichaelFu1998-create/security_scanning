def runnable_effects(self) -> List[Type[Effect]]:
        """Returns the runnable effect in the package"""
        return [cls for cls in self.effect_classes if cls.runnable]