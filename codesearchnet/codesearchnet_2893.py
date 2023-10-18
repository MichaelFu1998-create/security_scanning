def prepare(self, context):
    """Prepares the custom grouping for this component"""
    for stream_id, targets in self.targets.items():
      for target in targets:
        target.prepare(context, stream_id)