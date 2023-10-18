def invoke_hook_prepare(self):
    """invoke task hooks for after the spout/bolt's initialize() method"""
    for task_hook in self.task_hooks:
      task_hook.prepare(self.get_cluster_config(), self)