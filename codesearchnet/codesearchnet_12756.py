async def run(self, *args, data):
        """ run the function you want """
        cmd = self._get(data.text)

        try:
            if cmd is not None:
                command = self[cmd](*args, data=data)
                return await peony.utils.execute(command)

        except:
            fmt = "Error occurred while running function {cmd}:"
            peony.utils.log_error(fmt.format(cmd=cmd))