def launchapp(self, cmd, args=[], delay=0, env=1, lang="C"):
        """
        Launch application.

        @param cmd: Command line string to execute.
        @type cmd: string
        @param args: Arguments to the application
        @type args: list
        @param delay: Delay after the application is launched
        @type delay: int
        @param env: GNOME accessibility environment to be set or not
        @type env: int
        @param lang: Application language to be used
        @type lang: string

        @return: 1 on success
        @rtype: integer

        @raise LdtpServerException: When command fails
        """
        try:
            atomac.NativeUIElement.launchAppByBundleId(cmd)
            return 1
        except RuntimeError:
            if atomac.NativeUIElement.launchAppByBundlePath(cmd, args):
                # Let us wait so that the application launches
                try:
                    time.sleep(int(delay))
                except ValueError:
                    time.sleep(5)
                return 1
            else:
                raise LdtpServerException(u"Unable to find app '%s'" % cmd)