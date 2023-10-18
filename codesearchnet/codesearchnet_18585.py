def execute(self, arg_str='', **kwargs):
        """runs the passed in arguments and returns an iterator on the output of
        running command"""
        cmd = "{} {} {}".format(self.cmd_prefix, self.script, arg_str)
        expected_ret_code = kwargs.pop('code', 0)

        # any kwargs with all capital letters should be considered environment
        # variables
        environ = self.environ
        for k in list(kwargs.keys()):
            if k.isupper():
                environ[k] = kwargs.pop(k)

        # we will allow overriding of these values
        kwargs.setdefault("stderr", subprocess.STDOUT)

        # we will not allow these to be overridden via kwargs
        kwargs["shell"] = True
        kwargs["stdout"] = subprocess.PIPE
        kwargs["cwd"] = self.cwd
        kwargs["env"] = environ

        process = None
        self.buf = deque(maxlen=self.bufsize)

        try:
            process = subprocess.Popen(
                cmd,
                **kwargs
            )

            # another round of links
            # http://stackoverflow.com/a/17413045/5006 (what I used)
            # http://stackoverflow.com/questions/2715847/
            for line in iter(process.stdout.readline, b""):
                line = line.decode(self.encoding)
                self.buf.append(line.rstrip())
                yield line

            process.wait()
            if process.returncode != expected_ret_code:
                if process.returncode > 0:
                    raise RuntimeError("{} returned {} with output: {}".format(
                        cmd,
                        process.returncode,
                        self.output
                    ))

        except subprocess.CalledProcessError as e:
            if e.returncode != expected_ret_code:
                raise RuntimeError("{} returned {} with output: {}".format(
                    cmd,
                    e.returncode,
                    self.output
                ))

        finally:
            if process:
                process.stdout.close()