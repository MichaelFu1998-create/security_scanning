def locked_context(self, key=None, default=dict):
        """ Executor context is a shared memory object. All workers share this.
            It needs a lock. Its used like this:

            with executor.context() as context:
                visited = context['visited']
                visited.append(state.cpu.PC)
                context['visited'] = visited
        """
        assert default in (list, dict, set)
        with self._lock:
            if key is None:
                yield self._shared_context
            else:
                sub_context = self._shared_context.get(key, None)
                if sub_context is None:
                    sub_context = default()
                yield sub_context
                self._shared_context[key] = sub_context