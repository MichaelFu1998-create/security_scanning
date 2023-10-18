def do_exit(self, line):
        """
        Exit shell and shoebot
        """
        if self.trusted:
            publish_event(QUIT_EVENT)
        self.print_response('Bye.\n')
        return True