def release(self):
        """ Wraps Lock.release """
        self._lock.release()

        with self._stat_lock:
            self._locked = False
            self._last_released = datetime.now()