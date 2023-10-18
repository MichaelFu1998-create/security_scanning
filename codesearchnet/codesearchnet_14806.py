def serve_rpc(self):
        """Launches configured # of workers per loaded plugin."""
        if cfg.CONF.QUARK_ASYNC.rpc_workers < 1:
            cfg.CONF.set_override('rpc_workers', 1, "QUARK_ASYNC")

        try:
            rpc = service.RpcWorker(self.plugins)
            launcher = common_service.ProcessLauncher(CONF, wait_interval=1.0)
            launcher.launch_service(rpc, workers=CONF.QUARK_ASYNC.rpc_workers)

            return launcher
        except Exception:
            with excutils.save_and_reraise_exception():
                LOG.exception(_LE('Unrecoverable error: please check log for '
                                  'details.'))