def start(self):
        """Start the controller."""

        if self.mode == "manual":
            return

        if self.ipython_dir != '~/.ipython':
            self.ipython_dir = os.path.abspath(os.path.expanduser(self.ipython_dir))

        if self.log:
            stdout = open(os.path.join(self.ipython_dir, "{0}.controller.out".format(self.profile)), 'w')
            stderr = open(os.path.join(self.ipython_dir, "{0}.controller.err".format(self.profile)), 'w')
        else:
            stdout = open(os.devnull, 'w')
            stderr = open(os.devnull, 'w')

        try:
            opts = [
                'ipcontroller',
                '' if self.ipython_dir == '~/.ipython' else '--ipython-dir={}'.format(self.ipython_dir),
                self.interfaces if self.interfaces is not None else '--ip=*',
                '' if self.profile == 'default' else '--profile={0}'.format(self.profile),
                '--reuse' if self.reuse else '',
                '--location={}'.format(self.public_ip) if self.public_ip else '',
                '--port={}'.format(self.port) if self.port is not None else ''
            ]
            if self.port_range is not None:
                opts += [
                    '--HubFactory.hb={0},{1}'.format(self.hb_ping, self.hb_pong),
                    '--HubFactory.control={0},{1}'.format(self.control_client, self.control_engine),
                    '--HubFactory.mux={0},{1}'.format(self.mux_client, self.mux_engine),
                    '--HubFactory.task={0},{1}'.format(self.task_client, self.task_engine)
                ]
            logger.debug("Starting ipcontroller with '{}'".format(' '.join([str(x) for x in opts])))
            self.proc = subprocess.Popen(opts, stdout=stdout, stderr=stderr, preexec_fn=os.setsid)
        except FileNotFoundError:
            msg = "Could not find ipcontroller. Please make sure that ipyparallel is installed and available in your env"
            logger.error(msg)
            raise ControllerError(msg)
        except Exception as e:
            msg = "IPPController failed to start: {0}".format(e)
            logger.error(msg)
            raise ControllerError(msg)