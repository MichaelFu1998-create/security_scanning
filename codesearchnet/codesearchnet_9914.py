def result(self, timeout=None):
        """Gets the result of the task.

        Arguments:
            timeout: Maximum seconds to wait for a result before raising a
                TimeoutError. If set to None, this will wait forever. If the
                queue doesn't store results and timeout is None, this call will
                never return.
        """
        start = time.time()
        while True:
            task = self.get_task()
            if not task or task.status not in (FINISHED, FAILED):
                if not timeout:
                    continue
                elif time.time() - start < timeout:
                    continue
                else:
                    raise TimeoutError()

            if task.status == FAILED:
                raise task.result

            return task.result