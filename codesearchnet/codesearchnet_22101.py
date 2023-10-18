def reconcile(self, server):
        """
        Reconcile this collection with the server.
        """
        if not self.challenge.exists(server):
            raise Exception('Challenge does not exist on server')

        existing = MapRouletteTaskCollection.from_server(server, self.challenge)

        same = []
        new = []
        changed = []
        deleted = []

        # reconcile the new tasks with the existing tasks:
        for task in self.tasks:
            # if the task exists on the server...
            if task.identifier in [existing_task.identifier for existing_task in existing.tasks]:
                # and they are equal...
                if task == existing.get_by_identifier(task.identifier):
                    # add to 'same' list
                    same.append(task)
                    # if they are not equal, add to 'changed' list
                else:
                    changed.append(task)
            # if the task does not exist on the server, add to 'new' list
            else:
                new.append(task)

        # next, check for tasks on the server that don't exist in the new collection...
        for task in existing.tasks:
            if task.identifier not in [task.identifier for task in self.tasks]:
                # ... and add those to the 'deleted' list.
                deleted.append(task)

        # update the server with new, changed, and deleted tasks
        if new:
            newCollection = MapRouletteTaskCollection(self.challenge, tasks=new)
            newCollection.create(server)
        if changed:
            changedCollection = MapRouletteTaskCollection(self.challenge, tasks=changed)
            changedCollection.update(server)
        if deleted:
            deletedCollection = MapRouletteTaskCollection(self.challenge, tasks=deleted)
            for task in deletedCollection.tasks:
                task.status = 'deleted'
            deletedCollection.update(server)
        # return same, new, changed and deleted tasks
        return {'same': same, 'new': new, 'changed': changed, 'deleted': deleted}