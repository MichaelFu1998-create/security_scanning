def _swap_mode(self):
        """Toggle between ARM and Thumb mode"""
        assert self.mode in (cs.CS_MODE_ARM, cs.CS_MODE_THUMB)
        if self.mode == cs.CS_MODE_ARM:
            self.mode = cs.CS_MODE_THUMB
        else:
            self.mode = cs.CS_MODE_ARM