def scale_out(self, blocks=1, block_size=1):
        ''' Scale out the existing resources.
        '''
        self.config['sites.jetstream.{0}'.format(self.pool)]['flavor']
        count = 0
        if blocks == 1:
            block_id = len(self.blocks)
            self.blocks[block_id] = []
            for instance_id in range(0, block_size):
                instances = self.server_manager.create(
                    'parsl-{0}-{1}'.format(block_id, instance_id),  # Name
                    self.client.images.get('87e08a17-eae2-4ce4-9051-c561d9a54bde'),  # Image_id
                    self.client.flavors.list()[0],
                    min_count=1,
                    max_count=1,
                    userdata=setup_script.format(engine_config=self.engine_config),
                    key_name='TG-MCB090174-api-key',
                    security_groups=['global-ssh'],
                    nics=[{
                        "net-id": '724a50cf-7f11-4b3b-a884-cd7e6850e39e',
                        "net-name": 'PARSL-priv-net',
                        "v4-fixed-ip": ''
                    }])
                self.blocks[block_id].extend([instances])
                count += 1

        return count