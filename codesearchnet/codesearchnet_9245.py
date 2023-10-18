def __execute_initial_load(self):
        """
        Tasks that should be done just one time
        """

        if self.conf['phases']['panels']:
            tasks_cls = [TaskPanels, TaskPanelsMenu]
            self.execute_tasks(tasks_cls)
        if self.conf['phases']['identities']:
            tasks_cls = [TaskInitSortingHat]
            self.execute_tasks(tasks_cls)

        logger.info("Loading projects")
        tasks_cls = [TaskProjects]
        self.execute_tasks(tasks_cls)
        logger.info("Done")

        return