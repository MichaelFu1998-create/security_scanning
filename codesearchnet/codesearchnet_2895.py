def prepare(self, context, stream_id):
    """Invoke prepare() of this custom grouping"""
    self.grouping.prepare(context, self.source_comp_name, stream_id, self.task_ids)