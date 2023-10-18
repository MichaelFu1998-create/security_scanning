def prep_root_password(self, password=None, **kwargs):
        """
        Enters the root password prompt entries into the debconf cache
        so we can set them without user interaction.

        We keep this process separate from set_root_password() because we also need to do
        this before installing the base MySQL package, because that will also prompt the user
        for a root login.
        """
        r = self.database_renderer(**kwargs)
        r.env.root_password = password or r.genv.get('db_root_password')
        r.sudo("DEBIAN_FRONTEND=noninteractive dpkg --configure -a")
        r.sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password password {root_password}'")
        r.sudo("debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password {root_password}'")