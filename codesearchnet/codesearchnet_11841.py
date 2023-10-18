def record_manifest(self):
        """
        Returns a dictionary representing a serialized state of the service.
        """
        data = super(RabbitMQSatchel, self).record_manifest()
        params = sorted(list(self.get_user_vhosts())) # [(user, password, vhost)]
        data['rabbitmq_all_site_vhosts'] = params
        data['sites'] = list(self.genv.sites or [])
        return data