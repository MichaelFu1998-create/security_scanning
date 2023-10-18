def wait(self, sec=0.1):
        """ Wait for x seconds
            each wait command is 100ms """
        sec = max(sec, 0)
        reps = int(floor(sec / 0.1))
        commands = []
        for i in range(0, reps):
            commands.append(Command(0x00, wait=True))
        return tuple(commands)