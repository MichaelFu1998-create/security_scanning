def free_temp(self, v):
    """Release the GeneratedTempVar v so it can be reused."""
    self.used_temps.remove(v)
    self.free_temps.add(v)