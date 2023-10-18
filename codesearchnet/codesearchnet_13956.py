def run(self, inputcode, iterations=None, run_forever=False, frame_limiter=False, verbose=False,
            break_on_error=False):
        '''
        Executes the contents of a Nodebox/Shoebot script
        in current surface's context.

        :param inputcode: Path to shoebot source or string containing source
        :param iterations: None or Maximum amount of frames to run
        :param run_forever: If True then run until user quits the bot
        :param frame_limiter: If True then sleep between frames to respect speed() command.
        '''
        source = None
        filename = None

        if os.path.isfile(inputcode):
            source = open(inputcode).read()
            filename = inputcode
        elif isinstance(inputcode, basestring):
            filename = 'shoebot_code'
            source = inputcode

        self._load_namespace(self._namespace, filename)
        self._executor = executor = LiveExecution(source, ns=self._namespace, filename=filename)

        try:
            if not iterations:
                if run_forever:
                    iterations = None
                else:
                    iterations = 1
            iteration = 0

            event = None

            while iteration != iterations and not event_is(event, QUIT_EVENT):
                # do the magic

                # First iteration
                self._run_frame(executor, limit=frame_limiter, iteration=iteration)
                if iteration == 0:
                    self._initial_namespace = copy.copy(self._namespace)  # Stored so script can be rewound
                iteration += 1

                # Subsequent iterations
                while self._should_run(iteration, iterations) and event is None:
                    iteration += 1
                    self._run_frame(executor, limit=frame_limiter, iteration=iteration)
                    event = next_event()
                    if not event:
                        self._canvas.sink.main_iteration()  # update GUI, may generate events..

                while run_forever:
                    #
                    # Running in GUI, bot has finished
                    # Either -
                    #   receive quit event and quit
                    #   receive any other event and loop (e.g. if var changed or source edited)
                    #
                    while event is None:
                        self._canvas.sink.main_iteration()
                        event = next_event(block=True, timeout=0.05)
                        if not event:
                            self._canvas.sink.main_iteration()  # update GUI, may generate events..

                    if event.type == QUIT_EVENT:
                        break
                    elif event.type == SOURCE_CHANGED_EVENT:
                        # Debounce SOURCE_CHANGED events -
                        # gedit generates two events for changing a single character -
                        # delete and then add
                        while event and event.type == SOURCE_CHANGED_EVENT:
                            event = next_event(block=True, timeout=0.001)
                    elif event.type == SET_WINDOW_TITLE:
                        self._canvas.sink.set_title(event.data)

                    event = None  # this loop is a bit weird...
                    break

        except Exception as e:
            # this makes KeyboardInterrupts still work
            # if something goes wrong, print verbose system output
            # maybe this is too verbose, but okay for now

            import sys
            if verbose:
                errmsg = traceback.format_exc()
            else:
                errmsg = simple_traceback(e, executor.known_good or '')
            print >> sys.stderr, errmsg
            if break_on_error:
                raise