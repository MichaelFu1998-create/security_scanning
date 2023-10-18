def add_bolt(self, name, bolt_cls, par, inputs, config=None, optional_outputs=None):
    """Add a bolt to the topology"""
    bolt_spec = bolt_cls.spec(name=name, par=par, inputs=inputs, config=config,
                              optional_outputs=optional_outputs)
    self.add_spec(bolt_spec)
    return bolt_spec