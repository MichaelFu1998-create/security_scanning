def add_provider(self, share, provider, readonly=False):
        """Add a provider to the provider_map routing table."""
        # Make sure share starts with, or is '/'
        share = "/" + share.strip("/")
        assert share not in self.provider_map

        if compat.is_basestring(provider):
            # Syntax:
            #   <mount_path>: <folder_path>
            # We allow a simple string as 'provider'. In this case we interpret
            # it as a file system root folder that is published.
            provider = FilesystemProvider(provider, readonly)
        elif type(provider) in (dict,):
            if "provider" in provider:
                # Syntax:
                #   <mount_path>: {"provider": <class_path>, "args": <pos_args>, "kwargs": <named_args}
                prov_class = dynamic_import_class(provider["provider"])
                provider = prov_class(
                    *provider.get("args", []), **provider.get("kwargs", {})
                )
            else:
                # Syntax:
                #   <mount_path>: {"root": <path>, "redaonly": <bool>}
                provider = FilesystemProvider(
                    provider["root"], bool(provider.get("readonly", False))
                )
        elif type(provider) in (list, tuple):
            raise ValueError(
                "Provider {}: tuple/list syntax is no longer supported".format(provider)
            )
            # provider = FilesystemProvider(provider[0], provider[1])

        if not isinstance(provider, DAVProvider):
            raise ValueError("Invalid provider {}".format(provider))

        provider.set_share_path(share)
        if self.mount_path:
            provider.set_mount_path(self.mount_path)

        # TODO: someday we may want to configure different lock/prop
        # managers per provider
        provider.set_lock_manager(self.lock_manager)
        provider.set_prop_manager(self.prop_manager)

        self.provider_map[share] = provider
        # self.provider_map[share] = {"provider": provider, "allow_anonymous": False}

        # Store the list of share paths, ordered by length, so route lookups
        # will return the most specific match
        self.sorted_share_list = [s.lower() for s in self.provider_map.keys()]
        self.sorted_share_list = sorted(self.sorted_share_list, key=len, reverse=True)

        return provider