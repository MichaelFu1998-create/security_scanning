def get_program(self, label: str) -> moderngl.Program:
        """
        Get a program by its label

        Args:
            label (str): The label for the program

        Returns: py:class:`moderngl.Program` instance
        """
        return self._project.get_program(label)