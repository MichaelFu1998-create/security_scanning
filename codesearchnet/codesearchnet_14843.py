def get_resources(cls):
        """Returns Ext Resources."""
        job_controller = JobsController(
            directory.get_plugin())
        resources = []
        resources.append(extensions.ResourceExtension(
                         Jobs.get_alias(),
                         job_controller))
        return resources