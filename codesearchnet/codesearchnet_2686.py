def run(self, name, config, builder):
    """Builds the topology and submits it"""
    if not isinstance(name, str):
      raise RuntimeError("Name has to be a string type")
    if not isinstance(config, Config):
      raise RuntimeError("config has to be a Config type")
    if not isinstance(builder, Builder):
      raise RuntimeError("builder has to be a Builder type")
    bldr = TopologyBuilder(name=name)
    builder.build(bldr)
    bldr.set_config(config._api_config)
    bldr.build_and_submit()