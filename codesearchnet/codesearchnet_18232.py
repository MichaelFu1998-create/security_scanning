def run(self, start=True):
        """
        Connects to slack and enters the main loop.

        * start - If True, rtm.start API is used. Else rtm.connect API is used

        For more info, refer to
        https://python-slackclient.readthedocs.io/en/latest/real_time_messaging.html#rtm-start-vs-rtm-connect
        """
        # Fail out if setup wasn't run
        if not self.is_setup:
            raise NotSetupError

        # Start the web server
        self.webserver.start()

        first_connect = True

        try:
            while self.runnable:
                if self.reconnect_needed:
                    if not self.sc.rtm_connect(with_team_state=start):
                        return False
                    self.reconnect_needed = False
                    if first_connect:
                        first_connect = False
                        self.plugins.connect()

                # Get all waiting events - this always returns a list
                try:
                    events = self.sc.rtm_read()
                except AttributeError:
                    self.log.exception('Something has failed in the slack rtm library.  This is fatal.')
                    self.runnable = False
                    events = []
                except:
                    self.log.exception('Unhandled exception in rtm_read()')
                    self.reconnect_needed = True
                    events = []
                for e in events:
                    try:
                        self._handle_event(e)
                    except KeyboardInterrupt:
                        # Gracefully shutdown
                        self.runnable = False
                    except:
                        self.log.exception('Unhandled exception in event handler')
                sleep(0.1)
        except KeyboardInterrupt:
            # On ctrl-c, just exit
            pass
        except:
            self.log.exception('Unhandled exception')