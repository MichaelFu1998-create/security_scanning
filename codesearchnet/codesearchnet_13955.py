def _run_frame(self, executor, limit=False, iteration=0):
        """ Run single frame of the bot

        :param source_or_code: path to code to run, or actual code.
        :param limit: Time a frame should take to run (float - seconds)
        """
        #
        # Gets a bit complex here...
        #
        # Nodebox (which we are trying to be compatible with) supports two
        # kinds of bot 'dynamic' which has a 'draw' function and non dynamic
        # which doesn't have one.
        #
        # Dynamic bots:
        #
        # First run:
        # run body and 'setup' if it exists, then 'draw'
        #
        # Later runs:
        # run 'draw'
        #
        # Non Dynamic bots:
        #
        # Just have a 'body' and run once...
        #
        # UNLESS...  a 'var' is changed, then run it again.
        #
        #
        # Livecoding:
        #
        # Code can be 'known_good' or 'tenous' (when it has been edited).
        #
        # If code is tenous and an exception occurs, attempt to roll
        # everything back.
        #
        # Livecoding and vars
        #
        # If vars are added / removed or renamed then attempt to update
        # the GUI

        start_time = time()
        if iteration != 0 and self._speed != 0:
            self._canvas.reset_canvas()
        self._set_dynamic_vars()
        if iteration == 0:
            # First frame
            executor.run()
            # run setup and draw
            # (assume user hasn't live edited already)
            executor.ns['setup']()
            executor.ns['draw']()
            self._canvas.flush(self._frame)
        else:
            # Subsequent frames
            if self._dynamic:
                if self._speed != 0:  # speed 0 is paused, so do nothing
                    with executor.run_context() as (known_good, source, ns):
                        # Code in main block may redefine 'draw'
                        if not known_good:
                            executor.reload_functions()
                            with VarListener.batch(self._vars, self._oldvars, ns):
                                self._oldvars.clear()

                                # Re-run the function body - ideally this would only
                                # happen if the body had actually changed
                                # - Or perhaps if the line included a variable declaration
                                exec source in ns

                        ns['draw']()
                        self._canvas.flush(self._frame)
            else:
                # Non "dynamic" bots
                #
                # TODO - This part is overly complex, before live-coding it
                #        was just exec source in ns ... have to see if it
                #        can be simplified again.
                #
                with executor.run_context() as (known_good, source, ns):
                    if not known_good:
                        executor.reload_functions()
                        with VarListener.batch(self._vars, self._oldvars, ns):
                            self._oldvars.clear()

                            # Re-run the function body - ideally this would only
                            # happen if the body had actually changed
                            # - Or perhaps if the line included a variable declaration
                            exec source in ns
                    else:
                        exec source in ns

                    self._canvas.flush(self._frame)
        if limit:
            self._frame_limit(start_time)

        # Can set speed to go backwards using the shell if you really want
        # or pause by setting speed == 0
        if self._speed > 0:
            self._frame += 1
        elif self._speed < 0:
            self._frame -= 1