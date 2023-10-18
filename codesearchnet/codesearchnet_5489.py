def from_dict(name, values):
        '''
        Convert a dictionary of configuration values
        into a sequence of BlockadeContainerConfig instances
        '''

        # determine the number of instances of this container
        count = 1
        count_value = values.get('count', 1)
        if isinstance(count_value, int):
            count = max(count_value, 1)

        def with_index(name, idx):
            if name and idx:
                return '%s_%d' % (name, idx)
            return name

        def get_instance(n, idx=None):
            return BlockadeContainerConfig(
                with_index(n, idx),
                values['image'],
                command=values.get('command'),
                links=values.get('links'),
                volumes=values.get('volumes'),
                publish_ports=values.get('ports'),
                expose_ports=values.get('expose'),
                environment=values.get('environment'),
                hostname=values.get('hostname'),
                dns=values.get('dns'),
                start_delay=values.get('start_delay', 0),
                neutral=values.get('neutral', False),
                holy=values.get('holy', False),
                container_name=with_index(values.get('container_name'), idx),
                cap_add=values.get('cap_add'))

        if count == 1:
            yield get_instance(name)
        else:
            for idx in range(1, count+1):
                # TODO: configurable name/index format
                yield get_instance(name, idx)