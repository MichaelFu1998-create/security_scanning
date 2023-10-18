def new_source(self, source):
    """Adds a new source to the computation DAG"""

    source_streamlet = None
    if callable(source):
      source_streamlet = SupplierStreamlet(source)
    elif isinstance(source, Generator):
      source_streamlet = GeneratorStreamlet(source)
    else:
      raise RuntimeError("Builder's new source has to be either a Generator or a function")

    self._sources.append(source_streamlet)
    return source_streamlet