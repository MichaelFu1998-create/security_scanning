def release(self):
        """Release a semaphore, incrementing the internal counter by one.

        When the counter is zero on entry and another thread is waiting for it
        to become larger than zero again, wake up that thread.

        If the number of releases exceeds the number of acquires,
        raise a ValueError.

        """
        with self.__cond:
            if self.__value >= self._initial_value:
                raise ValueError("Semaphore released too many times")
            self.__value += 1
            self.__cond.notify()