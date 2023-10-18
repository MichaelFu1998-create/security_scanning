def _configure_users(self, site=None, full=0, only_data=0):
        """
        Installs and configures RabbitMQ.
        """

        site = site or ALL

        full = int(full)

        if full and not only_data:
            packager = self.get_satchel('packager')
            packager.install_required(type=SYSTEM, service=self.name)

        r = self.local_renderer

        params = self.get_user_vhosts(site=site) # [(user, password, vhost)]

        with settings(warn_only=True):
            self.add_admin_user()

        params = sorted(list(params))
        if not only_data:
            for user, password, vhost in params:
                r.env.broker_user = user
                r.env.broker_password = password
                r.env.broker_vhost = vhost
                with settings(warn_only=True):
                    r.sudo('rabbitmqctl add_user {broker_user} {broker_password}')
                    r.sudo('rabbitmqctl add_vhost {broker_vhost}')
                    r.sudo('rabbitmqctl set_permissions -p {broker_vhost} {broker_user} ".*" ".*" ".*"')
                    r.sudo('rabbitmqctl set_permissions -p {broker_vhost} {admin_username} ".*" ".*" ".*"')

        return params