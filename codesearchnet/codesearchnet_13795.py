def listener(self, sock, *args):
        '''Asynchronous connection listener. Starts a handler for each connection.'''
        conn, addr = sock.accept()
        f = conn.makefile(conn)
        self.shell = ShoebotCmd(self.bot, stdin=f, stdout=f, intro=INTRO)

        print(_("Connected"))
        GObject.io_add_watch(conn, GObject.IO_IN, self.handler)
        if self.shell.intro:
            self.shell.stdout.write(str(self.shell.intro)+"\n")
            self.shell.stdout.flush()
        return True