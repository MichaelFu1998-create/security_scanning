def handler(self, conn, *args):
        '''
        Asynchronous connection handler. Processes each line from the socket.
        '''
        # lines from cmd.Cmd
        self.shell.stdout.write(self.shell.prompt)
        line = self.shell.stdin.readline()
        if not len(line):
            line = 'EOF'
            return False
        else:
            line = line.rstrip('\r\n')
            line = self.shell.precmd(line)
            stop = self.shell.onecmd(line)
            stop = self.shell.postcmd(stop, line)
            self.shell.stdout.flush()
            self.shell.postloop()
            # end lines from cmd.Cmd
            if stop:
                self.shell = None
                conn.close()
            return not stop