def from_dict(values):
        '''
        Instantiate a BlockadeConfig instance based on
        a given dictionary of configuration values
        '''
        try:
            containers = values['containers']
            parsed_containers = {}
            for name, container_dict in containers.items():
                try:
                    # one config entry might result in many container
                    # instances (indicated by the 'count' config value)
                    for cnt in BlockadeContainerConfig.from_dict(name, container_dict):
                        # check for duplicate 'container_name' definitions
                        if cnt.container_name:
                            cname = cnt.container_name
                            existing = [c for c in parsed_containers.values() if c.container_name == cname]
                            if existing:
                                raise BlockadeConfigError("Duplicate 'container_name' definition: %s" % (cname))
                        parsed_containers[cnt.name] = cnt
                except Exception as err:
                    raise BlockadeConfigError(
                        "Container '%s' config problem: %s" % (name, err))

            network = values.get('network')
            if network:
                defaults = _DEFAULT_NETWORK_CONFIG.copy()
                defaults.update(network)
                network = defaults
            else:
                network = _DEFAULT_NETWORK_CONFIG.copy()

            return BlockadeConfig(parsed_containers, network=network)

        except KeyError as err:
            raise BlockadeConfigError("Config missing value: " + str(err))

        except Exception as err:
            # TODO log this to some debug stream?
            raise BlockadeConfigError("Failed to load config: " + str(err))