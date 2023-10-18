def tick(self):
        """Add one tick to progress bar"""
        self.current += 1
        if self.current == self.factor:
            sys.stdout.write('+')
            sys.stdout.flush()
            self.current = 0