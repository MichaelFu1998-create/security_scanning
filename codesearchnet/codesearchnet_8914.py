def queue_action(self, queue, *args, **kwargs):
        """Function that specifies the interaction with a
        :class:`.ResourceQueue` upon departure.

        When departuring from a :class:`.ResourceQueue` (or a
        :class:`.QueueServer`), this method is called. If the agent
        does not already have a resource then it decrements the number
        of servers at :class:`.ResourceQueue` by one. Note that this
        only applies to :class:`ResourceQueue's<.ResourceQueue>`.

        Parameters
        ----------
        queue : :class:`.QueueServer`
            The instance of the queue that the ``ResourceAgent`` will
            interact with.
        """
        if isinstance(queue, ResourceQueue):
            if self._has_resource:
                self._has_resource = False
                self._had_resource = True
            else:
                if queue.num_servers > 0:
                    queue.set_num_servers(queue.num_servers - 1)
                    self._has_resource = True
                    self._had_resource = False