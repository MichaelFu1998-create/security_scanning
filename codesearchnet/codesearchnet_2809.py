def add_spout(self, name, spout_cls, par, config=None, optional_outputs=None):
    """Add a spout to the topology"""
    spout_spec = spout_cls.spec(name=name, par=par, config=config,
                                optional_outputs=optional_outputs)
    self.add_spec(spout_spec)
    return spout_spec