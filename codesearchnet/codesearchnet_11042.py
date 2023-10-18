def clear_values(self, red=0.0, green=0.0, blue=0.0, alpha=0.0, depth=1.0):
        """
        Sets the clear values for the window buffer.

        Args:
            red (float): red compoent
            green (float): green compoent
            blue (float): blue compoent
            alpha (float): alpha compoent
            depth (float): depth value
        """
        self.clear_color = (red, green, blue, alpha)
        self.clear_depth = depth