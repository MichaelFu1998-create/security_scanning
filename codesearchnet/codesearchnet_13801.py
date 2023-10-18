def do_speed(self, speed):
        """
        rewind
        """
        if speed:
            try:
                self.bot._speed = float(speed)
            except Exception as e:
                self.print_response('%s is not a valid framerate' % speed)
                return
        self.print_response('Speed: %s FPS' % self.bot._speed)