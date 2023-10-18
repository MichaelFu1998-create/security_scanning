def create_local_renderer(self):
        """
        Instantiates a new local renderer.
        Override this to do any additional initialization.
        """
        r = super(ApacheSatchel, self).create_local_renderer()

        # Dynamically set values based on target operating system.
        os_version = self.os_version
        apache_specifics = r.env.specifics[os_version.type][os_version.distro]
        r.env.update(apache_specifics)

        return r