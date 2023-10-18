def validate_state_locations(self):
    """
    Names of all state locations must be unique.
    """
    names = map(lambda loc: loc["name"], self.locations)
    assert len(names) == len(set(names)), "Names of state locations must be unique"