def _run_once(self):
    """Run once, should be called only from loop()"""
    try:
      self.do_wait()
      self._execute_wakeup_tasks()
      self._trigger_timers()
    except Exception as e:
      Log.error("Error occured during _run_once(): " + str(e))
      Log.error(traceback.format_exc())
      self.should_exit = True