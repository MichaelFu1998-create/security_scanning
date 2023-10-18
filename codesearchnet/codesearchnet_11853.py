def push(self, components=None, yes=0):
        """
        Executes all satchel configurators to apply pending changes to the server.
        """
        from burlap import notifier
        service = self.get_satchel('service')
        self.lock()
        try:

            yes = int(yes)
            if not yes:
                # If we want to confirm the deployment with the user, and we're at the first server,
                # then run the preview.
                if self.genv.host_string == self.genv.hosts[0]:
                    execute(partial(self.preview, components=components, ask=1))

            notifier.notify_pre_deployment()
            component_order, plan_funcs = self.get_component_funcs(components=components)

            service.pre_deploy()
            for func_name, plan_func in plan_funcs:
                print('Executing %s...' % func_name)
                plan_func()
            self.fake(components=components)

            service.post_deploy()
            notifier.notify_post_deployment()

        finally:
            self.unlock()