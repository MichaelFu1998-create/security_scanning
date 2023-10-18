def has_gradient(self):
        """Returns true if _backward and _forward_backward can be called
        by an attack, False otherwise.

        """
        try:
            self.__model.gradient
            self.__model.predictions_and_gradient
        except AttributeError:
            return False
        else:
            return True