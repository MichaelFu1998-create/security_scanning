def configure_modrpaf(self):
        """
        Installs the mod-rpaf Apache module.

        https://github.com/gnif/mod_rpaf
        """
        r = self.local_renderer
        if r.env.modrpaf_enabled:
            self.install_packages()
            self.enable_mod('rpaf')
        else:
            if self.last_manifest.modrpaf_enabled:
                self.disable_mod('mod_rpaf')